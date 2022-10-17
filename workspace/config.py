from phidata.workspace import WorkspaceConfig

from workspace.settings import aws_region
from workspace.prd.settings import prd_env
from workspace.dev.aws_config import dev_aws_config
from workspace.dev.docker_config import dev_docker_config
from workspace.prd.aws_config import prd_aws_config
from workspace.prd.docker_config import prd_docker_config
from workspace.prd.k8s_config import prd_k8s_config

# -*- Define workspace resources using the WorkspaceConfig
workspace = WorkspaceConfig(
    default_env=prd_env,
    # Set to k8s after aws resources are created
    # default_config="k8s",
    aws_region=aws_region,
    aws=[
        dev_aws_config,
        prd_aws_config,
    ],
    k8s=[prd_k8s_config],
    docker=[
        dev_docker_config,
        # Uncomment to use create prd docker images
        prd_docker_config,
    ],
)
