"""
Training submitter

Facilitates (remote) training execution through the Azure ML service.
"""
import os
from azureml.core import Workspace, Experiment, ScriptRunConfig
from azureml.core.authentication import AzureCliAuthentication
from azureml.core.runconfig import RunConfiguration
from azureml.core.dataset import Dataset

newprofile = 'no'

# Define compute target for data engineering from AML
compute_target = 'alwaysoncluster'

# load Azure ML workspace
workspace = Workspace.from_config(auth=AzureCliAuthentication())

input_name_train = 'newsgroups_raw_train'
dataset_train = Dataset.get_by_name(workspace, name=input_name_train)

# Define datasets names
# Get environment from config yml for data engineering for full dataset
filepath = "environments/data_profiling/RunConfig/runconfig_data_profiling.yml"
input_name_train = 'newsgroups_raw_subset_train'

# Load run Config file for data prep
run_config = RunConfiguration.load(
    path=os.path.join(os.path.join(
        os.path.dirname(os.path.realpath(__file__)),
        "../..",
        filepath,
        )),
    name="dataprofiling"
)

est = ScriptRunConfig(
    source_directory=os.path.dirname(os.path.realpath(__file__)),
    run_config=run_config,
    arguments=[
        '--data_folder',
        dataset_train.as_named_input('train').as_mount(),
        '--local', 'no',
        '--new_profile', newprofile
    ],
)

# Define the ML experiment
experiment = Experiment(workspace, "historic-profile")
# Submit experiment run, if compute is idle, this may take some time')
run = experiment.submit(est)
