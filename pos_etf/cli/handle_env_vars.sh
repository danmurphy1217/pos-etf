
create_env_var() {
    export $1=$2
    echo "Set Env Var: " $1
    echo "Equal to: " $2
    return 1
}
envVarName=$1
valueForEnvVar=$2

create_env_var $envVarName $valueForEnvVar