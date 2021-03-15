#/bin/sh

refresh_token=`cat /web/NetApp_InstallBase/refresh_token`

curl --request POST \
  --url https://api.activeiq.netapp.com/v1/tokens/accessToken \
  --header 'accept: application/json' \
  --header 'content-type: application/json' \
  --data '{"refresh_token":"'$refresh_token'"}' > /web/NetApp_InstallBase/token_response

sed 's/.................//' /web/NetApp_InstallBase/token_response > /web/NetApp_InstallBase/token_response_1
sed 's/\".*$//g' /web/NetApp_InstallBase/token_response_1 > /web/NetApp_InstallBase/access_token

sed 's;^.*refresh_token\":\";;' /web/NetApp_InstallBase/token_response > /web/NetApp_InstallBase/token_response_1
sed 's/\".*$//g' /web/NetApp_InstallBase/token_response_1 > /web/NetApp_InstallBase/refresh_token
