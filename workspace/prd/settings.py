from typing import List
from typing_extensions import Literal

from workspace.settings import ws_name

# -*- Production settings

prd_env = "prd"
# Key for prd resources
prd_key = f"{ws_name}-{prd_env}"
# Tags for prd resources
prd_tags = {
    "Env": prd_env,
    "Project": ws_name,
}
# Domain for prd services like airflow and superset
prd_domain = "aws-snow.com"

# -*- EKS settings

# Production Subnets to use with the EKS cluster
prd_subnets: List[str] = []

# Node Group label for Services
services_ng_label = {
    "app_type": "service",
}
# Node Group label for Workers
workers_ng_label = {
    "app_type": "worker",
}

# How to distribute pods across EKS nodes
# "kubernetes.io/hostname" means spread across nodes
topology_spread_key: str = "kubernetes.io/hostname"
topology_spread_max_skew: int = 2
topology_spread_when_unsatisfiable: Literal[
    "DoNotSchedule", "ScheduleAnyway"
] = "DoNotSchedule"
