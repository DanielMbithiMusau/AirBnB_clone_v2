#!/usr/bin/env bash
# Check if enough arguments are provided

if [ $# -lt 4 ];
then
  echo "Usage: 0-transfer_file PATH_TO_FILE IP USERNAME PATH_TO_SSH_KEY"
  exit 1
else
  path_to_file=$1
  ip=$2
  username=$3
  path_to_ssh_key=$4

  scp -o StrictHostKeyChecking=no -i "$path_to_ssh_key" "$path_to_file" "$username"@"$ip":~/
fi
