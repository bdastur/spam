# Set ENV Variables
export PYANSI_USERNAME=$LOGNAME

if [[ -z ${PYANSI_PASSWORD} ]]; then
    echo -n "Remote Password for ${PYANSI_USERNAME}: "; read -s PYANSI_PASSWORD
    echo ""
    export PYANSI_PASSWORD=$PYANSI_PASSWORD
fi

if [[ -z ${PYANSI_VAULT_PASSWORD} ]]; then
    echo -n "Vault Password: "; read -s PYANSI_VAULT_PASSWORD
    echo ""
    export PYANSI_VAULT_PASSWORD=$PYANSI_VAULT_PASSWORD
fi

export ANSIBLE_HOST_KEY_CHECKING=False

curr_dir=$(pwd)
testdir_name=${curr_dir##*/}

if [[ $testdir_name != "test" ]]; then
    echo "Current directory is not \"test\"."
    return 
fi

pyansible_path=${curr_dir%/*}                
export PYTHONPATH="$PYTHONPATH:${pyansible_path}"
