class_name VelocityComponent
extends Component

@export var direction: Vector2 = Vector2.ZERO
@export var speed: float = 200.00


func _init(ispd: float = 200.00, idir: Vector2 = Vector2.ZERO) -> void:
	self.direction = idir
	self.speed = ispd
