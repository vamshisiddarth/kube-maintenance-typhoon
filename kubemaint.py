import boto3,os,sys,json,pprint
from kubernetes import client, config
import kubernetes.client

dir_path = os.path.dirname(os.path.realpath(__file__))

# Declaring the AWS account details
if sys.argv[1] == "prod":
  account_id = "<replace_account_id>"
  env = "prod"
elif sys.argv[1] == "stage":
  account_id = "<replace_account_id>"
  env = "stage"
elif sys.argv[1] == "dev":
  account_id = "<replace_account_id>"
  env = "dev"
else:
  print("Invalid Source Environment")


# Configuring the Kubeconfig for the target environment
kubeconfig = dir_path + "/../../_kubeconfig/" + env + "/kubeconfig"


# aws config
session = boto3.Session(profile_name='<repalce_profile_name>')

sts_client = session.client('sts')
assumed_role_object=sts_client.assume_role(
  RoleArn="arn:aws:iam::" + account_id + ":role/Administrator",
  RoleSessionName="AssumeRoleSession",
)

credentials=assumed_role_object['Credentials']

ec2_resource=session.client(
  'ec2',
  aws_access_key_id=credentials['AccessKeyId'],
  aws_secret_access_key=credentials['SecretAccessKey'],
  aws_session_token=credentials['SessionToken'],
)

# Configs can be set in Configuration class directly or using helper utility
config.load_kube_config(kubeconfig)
v1 = kubernetes.client.CoreV1Api()

response = ec2_resource.describe_instances()

# Node table which will have all the running instances.
nodetable = []

for reservation in response["Reservations"]:
  for instance in reservation["Instances"]:
    try:
     nodeip = instance["PrivateIpAddress"]
     # Add Running nodes to the list to be compared later
     nodetable.append(nodeip)
    except:
      print("Instance Terminated")

listnodes = v1.list_node()
for i in listnodes.items:
  node = i.metadata.name
  iplist = node.split("-")
  ip = "."
  ip = ip.join(iplist[1:])
  if ip in nodetable:
    print("Node is in the Ready State")
  else:
    print(ip + "- Removing the node from kubernetes")
    v1.delete_node(node)

