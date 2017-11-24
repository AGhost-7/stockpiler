# API
Backend used by stockpiler.

## Authentication
After being authenticated, you will need to pass in your authentication token
in the http `Authorization` header like so:

```
Authorization: Bearer eyJhbGciOiJIUzI1NiIXVCJ9TJVA95OrM7E20RMHrHDcEfxjoYZgeFONFh7HgQ
```

## Pagination

All list endpoints have an optional `limit` and `offset` query parameter. By
default, `limit` is set to 20 (maximum of 100), and `offset` is by default 0.

## Endpoints

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

Sends an email where the url will be `BASE_URL + '/email-confirmation/' + TOKEN`.

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

#### Password Reset

##### Initialize
```
POST /v1/users/password-reset
```

Request body:
```
{
	"email": "the-users-email@gmail.com"
}
```

Sends an email where the url will be `BASE_URL + '/password-reset/' + TOKEN`.

##### Fetch
```
GET /v1/users/password-reset/:token
```

Response body:
```
{
	"token": "some uuid",
	"user_id": "some other uuid",
	"user": {
		"id": "some id",
		"email": "foo@bar.com",
		"email_confirmed": true
	}
}
```

Will return an error if the token has expired or does not exit.

##### Submit

```
POST /v1/users/password-reset/:token
```

Request body:
```
{
	"password": "mypassword"
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
	"owner_id": "",
	"name": "My Store"
}
```

#### Listing all Locations

```
GET /v1/locations
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
	"hardware_id": "e5bda6854daf8b61f8f181dbdec624f357b9efb8",
	"mac_address": "01:23:45:67:89:ab",
	"location_id": "example",
	"name": "My device name"
}
```

The hardware id is an HMAC of the MAC address of the machine and a secret.

#### De-register a device

```
DELETE /v1/locations/:locationId/devices/:deviceId
```

## Developing


To spin up services that the api is dependent on, run the following:
```
docker-compose up
```

Then, in a separate terminal, run the following:
```
virtualenv env
. env/bin/activate
pip install -r requirements.txt
pip install --editable .
api_create_tables
api
```
