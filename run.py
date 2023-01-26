import oci
import os
import time
config = {
    "user"="ocid1.user.oc1..aaaaaaaaul4cbqzowr4x5bnmsdmlqpo3onbs2ekwqb55yhnbh3izmksgr5ha",
    "fingerprint"="e9:c9:3d:07:cd:33:3c:3a:99:08:58:5b:56:7b:36:67",
    "tenancy"="ocid1.tenancy.oc1..aaaaaaaasnvm3ufpikguqeurze3z6ek5pgbsg2uiqtkfqha5qxplzbqqbm5a",
    "region"="ap-singapore-1",
    "key_file": "oci_private.pem
}

instance_name = 'instance-20230107-1323'
shape = 'VM.Standard.E2.1.Micro'
availability_domain = 'vOeV:AP-SINGAPORE-1-AD-1'
compartment_id= 'ocid1.tenancy.oc1..aaaaaaaasnvm3ufpikguqeurze3z6ek5pgbsg2uiqtkfqha5qxplzbqqbm5a'
image_id= 'ocid1.image.oc1.ap-singapore-1.aaaaaaaaylr7uotjuy4rbyfe2tm6icj6vwr77goh3rzvmcwzxovunkejypsa'
subnet_id = 'ocid1.subnet.oc1.ap-singapore-1.aaaaaaaavnabp2lchaixly3e4idw4kzhan3hng73sou4voxnr5zodncfwsnq'
ssh_authorized_keys = 'ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQCP5RgnI5+rQLcraEfU/59MZLqE5tXZQRiLoZ1J42wt9nrPh2uy1ReVUQzzX3hXQRbOc62Og+XCVEMILvgFa+1bQysFev1jQCKeG1bqufJniVT9heWksKy85aFuCd8tnCSpeCjFoSnCohySpeh0dceIjw/mimhr//+74806HQIp6j/w2dIpj4jc4ArmgEvxdocR8Oi4F+C1hQ1uJCsb8dMzV/g9csXbW2+gktbQEpiO+XgRbC4CVBgT6nZGF5RhVwDyLMc6ec/4gvRfMcy24b+dDQnVR7/JdpTx2FDS2ALwr6u6/+XNsPpnxAAsN0mKiviUrffQ1xCcoh0cXil7BsXR rsa-key-20230107'
bootVolumeSizeInGBs = 50
bootVolumeVpusPerGB = 10
isPvEncryptionInTransitEnabled = True

compute_client = oci.core.ComputeClient(config)
while True:
  # Create a VM
  try:  
    vm_response = compute_client.launch_instance(
        oci.core.models.LaunchInstanceDetails(
            compartment_id=compartment_id,
            display_name = instance_name,
            image_id=image_id,
            shape=shape,
            subnet_id=subnet_id,
            availability_domain=availability_domain,
            is_pv_encryption_in_transit_enabled=True,
            metadata={
                "ssh_authorized_keys": ssh_authorized_keys
            }
        )
    )
  except oci.exceptions.ServiceError as er:
      print(er.message)
      print("waiting for 10s")
      time.sleep(10)
      continue
  
  vm = vm_response.data
  print("Created VM:", vm.id)
  # Wait for the VM to reach the "Running" state
  compute_client.get_instance(vm.id).wait_until(
      oci.core.models.Instance.LIFECYCLE_STATE_RUNNING,
      max_wait_seconds=10
  )
  print("VM is running")
