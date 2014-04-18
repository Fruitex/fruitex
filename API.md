# Fruitex API v1.0


## Overview

### Pagination
Any request that returns more than one item is paginated. By default, each page contains 10 items. To change page size, set parameter `page_size={size}`. To specify the requested page, set parameter `page={number}`.

### Response Type
All requests support a human-friendly format `api` and an application-friendly format `json`. The default value is `api`. To specify the response type, set parameter `format={type}`.

### Error Codes
`TODO`.

### Ordering
Reverse ordering is allowed by adding a minus sign `-` before the parameter value. E.g. `/invoices/?ordering=-when_created` will return all invoices in reverse chronological order. Multiple ordering is also allowed. Parameter values are comma separated as follows: `/invoices/?ordering=-when_created,total`.


## URL Schemas

### Account

Resource | Method | Status | Description
--- | --- | --- | ---
[/users](#users) | GET | *Implemented* | Returns a list of users.
[/users/{id}](#) | GET | *Implemented* | Returns the user with given id.
[/users/current](#) | GET | *[Implemented](https://github.com/Fruitex/fruitex/commit/3e3666f387605aa152bbfa7fedd2a206147f8c02)* | Returns the current user.

### Shop

Resource | Method | Status | Description
--- | --- | --- | ---
[/stores](#) | GET | *Implemented* | Returns a list of stores.
[/stores/{id}](#) | GET | *Implemented* | Returns the store with given id.
[/stores/{id}/categories](#) | GET | *Implemented* | Returns the store categories list.
[/stores/{id}/store_customizations](#) | GET | *Planned* | Returns the store customization settings.
~~[/categories](#)~~ | GET | *Deprecated* | Returns a list of categories.
[/categories/{id}](#) | GET | *Implemented* | Returns the category with given id.
[/categories/{id}/items](#) | GET | *Implemented* | Returns a list of items within the category.
~~[/items](#)~~ | GET | *Deprecated* | Returns a list of items.
[/items/{id}](#) | GET | *Implemented* | Returns the item with given id.

### Order

Resource | Method | Status | Description
--- | --- | --- | ---
[/invoices](#) | GET | *Implemented* | Returns a list of invoices in reverse chronological order.
[/invoices/{id}](#invoices) | GET | *Implemented* | Returns the invoice with given id.
[/invoices/{id}/orders](#invoices) | GET | *Implemented* | Returns the orders belongs to the given invoice.
[/orders](#orders) | GET | *Implemented* | Returns a list of orders in reverse chronological order.
[/orders/{id}](#orders) | GET | *Implemented* | Returns the order with given id.
  | PUT | *Planned* | Updates to an order. Used to update order status.
[/orders/{id}/order_items](#) | GET | *Implemented* | Returns the given order's order items.
~~[/order_items](#)~~ | GET | *Deprecated* | Returns a list of order items.
[/order_items/{id}](#) | GET | *Implemented* | Returns the order item with given id.
  | PUT | *Planned* | Partial updates to an order item. Used to update order item status.

### Delivery

Resource | Method | Status | Description
--- | --- | --- | ---
[/delivery_windows](#) | GET | *Implemented* | Returns a list of delivery windows.
[/delivery_windows/{id}](#) | GET | *Implemented* | Returns the delivery window with given id.
[/delivery_buckets](#delivery-buckets) | GET | *Implemented* | Returns a list of delivery buckets in reverse chronological order.
[/delivery_buckets/{id}](#) | GET | *Implemented* | Returns the delivery bucket with given id.
[/delivery_buckets/{id}/orders](#) | GET | *Implemented* | Returns the delivery bucket orders with given delivery bucket id.


## API Details

### Users

#### Permissions

Anyone can access this endpoint.

#### Parameters

Key | Type | Description | Example
--- | --- | --- | --- | ---
`ordering` | `string` | Order users by `date_joined`, or `last_login`. | /users/?ordering=-date_joined

#### Fields

`TODO`

### Invoices

#### Permissions

- list: `driver` only
- retrieve: 
	- guest order: anyone
	- user order: `owner` or `driver`


### Orders

#### Permissions

- list: `driver` only
- retrieve: 
	- guest order: anyone
	- user order: `owner` or `driver`

#### Parameters

Key | Type | Description | Example
--- | --- | --- | ---
`ordering` | `string` | Order orders by `when_created`, `when_updated`, or `subtotal`. | /orders/?ordering=subtotal
`status` | `string` | Filter orders by `status`. Possible values are `CANC`, `PEND`, `PAID`, `POD` | /orders/?status=PEND

#### Fields

`TODO`

### Delivery Buckets

#### Permissions

- list: `manager` only
- retrieve: `manager` or `assignee`
