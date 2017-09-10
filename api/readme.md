## API
Note: After being authenticated, you will need to pass in your authentication
token in the http `Authorization` header like so:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJVA95OrM7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```

### User

#### Register a new user

```
POST /v1/users/register
```

Request body:
```
{
	"email": "aghost-7@example.com",
	"password": "testing123"
}
```

#### Email confirmation

```
GET /v1/users/confirm-email/:id
```

#### Login

```
POST /v1/users/login
```

Request body:
```
{
	"email": "aghost-7@example.com",
	"password": "testing123"
}
```

### Location

#### Creating a Location
```
POST /v1/locations
```

Request body:
```
{
	"ownerId": "",
	"name": "My Store"
}
```

### Location Members

#### Grant Access to a Location

```
POST /v1/locations/:locationId/members/:userId
```

#### Revoke Access to a Location

```
DELETE /v1/locations/:locationId/members/:userId
```

### Item

#### Create a new item

```
POST /v1/locations/:locationId/items
```

Request body:
```
{
	"name": "carrots",
	"quantity": 100000000
}
```

Note: Weight is stored in milligrams.

#### Update an item

```
PUT /v1/locations/:locationId/items/:id
```

Request body:

```
{
	"name": "carrots",
	"quantity": 100000
}
```

Note: Devices can only decrement the quantity. Attempting to increase the
quantity or change the name of an inventory item will result in a 400 response.

#### List items

```
GET /v1/locations/:locationId/items
```

Query parameters:
- `page`: Pagination is done in chunks of 20. If not specifed this will default
to displaying the first page.

### Item Logs

```
GET /v1/locations/:locationId/items/:itemId/logs
```

Query parameters:
- `page`: Pagination is done in chunks of 20. If not specifed this will default
to displaying the first page.

### Device
A device represents a piece of hardware which is connected via bluetooth
initially.

#### Register a device
When the device wants to register, it connects to the user's machine first and
will then be associated to a location.

```
POST /v1/locations/:locationId/devices
```

Request body:
```
{
	"hardwareId": "e5bda6854daf8b61f8f181dbdec624f357b9efb8",
	"macAddress": "01:23:45:67:89:ab",
	"locationId": "example",
	"name": "My device name"
}
```

The hardware id is an HMAC of the MAC address of the machine and a secret.

#### De-register a device

```
DELETE /v1/locations/:locationId/devices/:deviceId
```

## Developing

```
sudo pip install -r requirements.txt
docker-compose up
```

