class_name HealthComponent
extends Component

@export var maximum: float = 100.0
@export var current: float = maximum


func _init(imax: float = 100.0) -> void:
	self.maximum = imax
	self.current = imax
