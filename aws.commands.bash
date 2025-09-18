aws configure

# Vai pedir o Access Key e o Secret Key, são disponíveis na sessão de usuários no IAM

aws dynamodb create-table \
  --table-name Appointments \
  --attribute-definitions AttributeName=date,AttributeType=S AttributeName=time,AttributeType=S \
  --key-schema AttributeName=date,KeyType=HASH AttributeName=time,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST
