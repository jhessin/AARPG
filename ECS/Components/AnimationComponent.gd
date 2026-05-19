class_name AnimationComponent
extends Component

var animator: AnimationPlayer
var sprite: Sprite2D


func _init(anim: AnimationPlayer, isprite: Sprite2D) -> void:
	animator = anim
	self.sprite = isprite
