from phidata.infra.docker.resource.image import DockerImage
from workspace.settings import (
    ws_name,
    use_cache,
    airflow_enabled,
    jupyter_enabled,
    databox_enabled,
    data_platform_dir_path,
)

# -*- Dev images

dev_images = []

# Shared image params
image_tag = "dev"
image_repo = "phidata"  # Set your image repo
image_suffix = ws_name  # Set your image name suffix
skip_docker_cache = False  # Skip docker cache when building images
pull_docker_images = False  # Force pull images during FROM
push_docker_images = False  # Push images to repo after building

# Airflow image
dev_airflow_image = DockerImage(
    name=f"{image_repo}/airflow-{image_suffix}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/dev/images/airflow.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    # use_cache=False will recreate the image every time you run `phi ws up`
    # eg: `CACHE=f phi ws up`
    use_cache=use_cache,
)

if airflow_enabled:
    dev_images.append(dev_airflow_image)

# Jupyter image
dev_jupyter_image = DockerImage(
    name=f"{image_repo}/jupyter-{image_suffix}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/dev/images/jupyter.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    use_cache=use_cache,
)

if jupyter_enabled:
    dev_images.append(dev_jupyter_image)

# Databox image
dev_databox_image = DockerImage(
    name=f"{image_repo}/databox-{image_suffix}",
    tag=image_tag,
    path=str(data_platform_dir_path),
    dockerfile="workspace/dev/images/databox.Dockerfile",
    print_build_log=True,
    pull=pull_docker_images,
    push_image=push_docker_images,
    skip_docker_cache=skip_docker_cache,
    use_cache=use_cache,
)

if databox_enabled:
    dev_images.append(dev_databox_image)
