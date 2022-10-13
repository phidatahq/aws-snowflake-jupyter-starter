from phidata.asset.aws.s3.csv_dataset import S3DatasetCsv
from phidata.task import TaskArgs, task
from phidata.workflow import Workflow
from phidata.utils.log import logger

from workflows.env import AIRFLOW_ENV
from workflows.buckets import DATA_S3_BUCKET

##############################################################################
# As workflow for calculating daily active users using s3 and athena
##############################################################################

# Step 1: Define datasets for storing user activity and daily active users
user_activity_table = S3DatasetCsv(
    table=f"user_activity_{AIRFLOW_ENV}",
    database="users",
    write_mode="overwrite_partitions",
    bucket=DATA_S3_BUCKET,
)
daily_active_users_table = S3DatasetCsv(
    table=f"daily_active_users_{AIRFLOW_ENV}",
    database="users",
    write_mode="overwrite_partitions",
    bucket=DATA_S3_BUCKET,
)

# Step 2: Create task to download user activity data and write to s3 dataset
@task
def load_user_activity(**kwargs) -> bool:
    """
    Download user activity data and write to s3
    """
    import pandas as pd

    args: TaskArgs = TaskArgs.from_kwargs(kwargs)

    run_ds = args.run_date.strftime("%Y-%m-%d")
    logger.info(f"Downloading user activity for: ds={run_ds}")
    _df = pd.read_csv(
        "https://raw.githubusercontent.com/phidatahq/demo-data/main/dau_2021_10_01.csv"
    )
    _df.reset_index(drop=True, inplace=True)
    _df.set_index("ds", inplace=True)
    print(_df.head())

    return user_activity_table.write_pandas_df(_df, create_database=True)


# Step 3: Create task to calculate daily active users and write to s3 dataset
@task
def load_daily_active_users(**kwargs) -> bool:
    """
    Calculate daily active users and write to s3
    """

    args: TaskArgs = TaskArgs.from_kwargs(kwargs)

    run_ds = args.run_date.strftime("%Y-%m-%d")
    logger.info(f"Calculating daily active users for: ds={run_ds}")
    return daily_active_users_table.create_from_query(
        sql=f"""
            SELECT
                ds,
                SUM(CASE WHEN is_active=1 THEN 1 ELSE 0 END) AS active_users
            FROM users.user_activity
            GROUP BY ds
            """,
        wait=True,
        drop_before_create=True,
    )


# Step 4: Instantiate the tasks
download_user_activity = load_user_activity()
load_dau = load_daily_active_users()

# Step 5: Create a Workflow to run tasks
dau_aws = Workflow(
    name="dau_aws",
    tasks=[download_user_activity, load_dau],
    # the graph orders load_dau to run after download_user_activity
    graph={load_dau: [download_user_activity]},
    # the outputs of this workflow
    outputs=[user_activity_table, daily_active_users_table],
)

# Step 6: Create a DAG to run the workflow on a schedule
dag = dau_aws.create_airflow_dag(
    schedule_interval="@daily",
    is_paused_upon_creation=True,
)
