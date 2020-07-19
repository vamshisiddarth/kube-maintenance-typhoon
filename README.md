# kube-maintenance-typhoon

This script will list all the instances and search for the instances in `shutting-down` state and get its `PrivateDnsName`. This is used for removing this node from the kubernetes cluster to avoid the application down time.

#### Goal

We have been using the Typhoon kubernetes cluster in our environment with spot instances which works great. A few times, we faced the issue with the Spot instances being terminated due to "" error and the nodes go into the "NotReady" state and pods running on it goes into the "Terminating" state. Untill these Terminating pods are completely terminated, we cannot have new pods created which resulted in application down time. We have been using this script which will check all the running instances and checks the nodes against this list and deletes the nodes which doesn't match the running instances.

This can be scheduled as either a cron job or a aws lambda function.

#### prerequisites

The script will be looking for file credentials.txt which will have the aws credentails. It should be similar to the below.

```bash
[infosec]
aws_access_key_id = AKIATDAKDMFR857JE
aws_secret_access_key = bfjdcklsdcpooo32r020rf
region = eu-west-1
```

#### Usage

```bash
AWS_SHARED_CREDENTIALS_FILE="./credentials.txt" python kubemaint.py dev
Node is in the Ready State
Node is in the Ready State
Node is in the Ready State
Node is in the Ready State
Node is in the Ready State
Node is in the Ready State
Instance Terminated
192.123.1.0- Removing the node from kubernetes
```



