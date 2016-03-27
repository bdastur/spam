# Set ENV Variables
# Username, password, Ledger config path
export PYANSI_USERNAME=$LOGNAME

if [[ -z ${PYANSI_PASSWORD} ]]; then
    echo -n "Remote Password for ${PYANSI_USERNAME}: "; read -s PYANSI_PASSWORD
    echo ""
    export PYANSI_PASSWORD=$PYANSI_PASSWORD
fi

export ANSIBLE_HOST_KEY_CHECKING=False


