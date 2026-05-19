class_name State
extends Node

## Stores a reference to the player that this state belongs to
static var player: Player


func enter() -> void:
	"""
	What happens when the player enters this state?
	"""


func exit() -> void:
	"""
	What happens when the player exits this state?
	"""


func process(_delta: float) -> State:
	"""
	What happens during the _process update in this state?
	"""
	return null


func physics(_delta: float) -> State:
	"""
	What happens during the _physics_process update in this state?
	"""
	return null


func handle_input(_event: InputEvent) -> State:
	"""
	What happens with input events in this State?
	"""
	return null
