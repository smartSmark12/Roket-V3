## actions

- spawn
- explode
- heal - heal ship
- damage - deal damage to affected target
- param - hard-set ship parameter (size, speed, lives)

### params
- spawn [ObjectName:str, position:tuple]
- explode []
- heal [amount:int]
- damage [amount:int]
- param [paramName:str, value:any]

## damage source
- roket - damages only roket
- enemy - damages (interacts with) enemies
- both - interacts with both (careful with spawning collider??)