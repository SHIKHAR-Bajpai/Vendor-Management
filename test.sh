
BASE_URL="http://127.0.0.1:5000"
TOKEN=""

echo "Registering vendor..."
curl -X POST "$BASE_URL/auth/register" -H "Content-Type: application/json" -d '{"name": "Test Vendor","email": "test@example.com","password": "password123"}'
echo -e "\n"

echo "Logging in..."
TOKEN=$(curl -X POST "$BASE_URL/auth/login" -H "Content-Type: application/json" -d '{"email": "test@example.com","password": "password123"}' | jq -r '.access_token')
echo "Token: $TOKEN"
echo -e "\n"

echo "Creating a shop..."
curl -X POST "$BASE_URL/auth/create" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"shop_name": "Test Shop","owner_name": "John Doe","type": "Grocery","latitude": 28.3806453,"longitude": 79.4038268}'
echo -e "\n"

echo "Fetching shops..."
curl -X GET "$BASE_URL/shops" -H "Authorization: Bearer $TOKEN"
echo -e "\n"

SHOP_ID=1

echo "Updating shop..."
curl -X PUT "$BASE_URL/shops/update/$SHOP_ID" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"shop_name": "Updated Shop Name"}'
echo -e "\n"

echo "Deleting shop..."
curl -X DELETE "$BASE_URL/shops/delete/$SHOP_ID" -H "Authorization: Bearer $TOKEN"
echo -e "\n"

echo "Fetching nearby shops..."
curl -X GET "$BASE_URL/shops/nearby?latitude=28.3806453&longitude=79.4038268&radius=5000"
echo -e "\n"

echo "Updating vendor..."
curl -X PUT "$BASE_URL/auth/update" -H "Content-Type: application/json" -H "Authorization: Bearer $TOKEN" -d '{"name": "Updated Vendor Name"}'
echo -e "\n"

echo "Deleting vendor..."
curl -X DELETE "$BASE_URL/auth/delete" -H "Authorization: Bearer $TOKEN"
echo -e "\n"
