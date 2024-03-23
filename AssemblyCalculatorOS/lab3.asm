.data
	max_values: .word 5			# Maximum number of values allowed
	n_values: .word 11			# Number of values entered by the user
	even_sum: .word 0			# Sum of even values
	int_values: .space 20			# Array to store entered values
	prompt: .asciiz "How many values do you want to enter? "			# Prompt for entering number of values
	maxValuesMsg: .asciiz " is the maximum amount allowed\n"			# Error message for exceeding max values
	valuePrompt: .asciiz "Enter value "			# Prompt for entering each value
	valuesMsg: .asciiz "The values are ["			# Message indicating the start of printed values
	evenSumMsg: .asciiz "]\nThe sum of even values is "	# Message indicating the start of even sum
	comma: .asciiz ", "			# Comma separator for printed values
	colon: .asciiz ": "			# Colon separator for prompts
	newline: .asciiz "\n"			# Newline character

.text
.globl main

main:
	# Initialize registers
	# $t0: Address register
	# $t1: Temporary storage
	# $t2: Counter/index for loops
	# $t3: Sum of even numbers

	la $t0, n_values		# Load the address of n_values
	lw $t1, max_values		# Load max_values

input_count:
	# Get number of values to input
	li $v0, 4			# Print string syscall
	la $a0, prompt			# Load address of input prompt
	syscall

	li $v0, 5			# Read integer syscall
	syscall
	sw $v0, 0($t0)			# Store the result in n_values

	lw $t2, 0($t0)			# Load n_values into $t2
	ble $t2, $t1, input_values	# Branch if n_values is less than or equal to max_values

	# If n_values is greater than max_values, print error message and prompt again
	li $v0, 1			# Print integer syscall
	move $a0, $t1			# Load max_values into $a0
	syscall

	li $v0, 4			# Print string syscall
	la $a0, maxValuesMsg		# Load address of maxValuesMsg
	syscall
	j input_count			# Jump back to input_count to ask again

input_values:
	# Read the values into the array
	la $t0, int_values		# Load base address of int_values
	li $t2, 0			# Reset the counter/index
	lw $t1, n_values		# Load n_values into $t1

read_values_loop:
	blt $t2, $t1, read_value	# Continue loop if $t2 < $t1
	j calculate_even_sum		# Otherwise, jump to calculate_even_sum

read_value:
	li $v0, 4			# Print string syscall
	la $a0, valuePrompt		# Load address of valuePrompt
	syscall
	li $v0, 1			# Print integer syscall
	add $a0, $t2, 1			# Add 1 to index for user-friendly display
	syscall
	li $v0, 4			# Print string syscall
	la $a0, colon			# Load address of colon
	syscall

	li $v0, 5			# Read integer syscall
	syscall
	sw $v0, 0($t0)			# Store value in int_values array
	addi $t0, $t0, 4		# Move to next space in array
	addi $t2, $t2, 1		# Increment index
	j read_values_loop		# Jump back to read_values_loop

calculate_even_sum:
	li $t2, 0			# Reset index to zero
	la $t0, int_values		# Load base address of int_values
	lw $t1, n_values		# Load n_values into $t1

sum_even_values_loop:
	blt $t2, $t1, continue_sum	# Check if the counter is less than n_values
	j print_values			# Jump to print_values if not

continue_sum:
	lw $a0, 0($t0)			# Load current value
	andi $a0, $a0, 1		# Check if value is even
	bne $a0, $zero, skip_add	# If odd, skip addition
	lw $a0, 0($t0)			# Load even value
	add $t3, $t3, $a0		# Add even value to sum

skip_add:
	addi $t0, $t0, 4		# Move to next integer in array
	addi $t2, $t2, 1		# Increment counter
	j sum_even_values_loop		# Continue loop

print_values:
	li $v0, 4			# Print string syscall
	la $a0, valuesMsg		# Load address of valuesMsg
	syscall

	la $t0, int_values		# Reset $t0 to start of the array
	li $t2, 0			# Reset index to zero
	lw $t1, n_values		# Load n_values into $t1

print_loop:
	blt $t2, $t1, print_next	# Continue loop if not all values are printed
	j finish_print_array		# Otherwise, jump to finish_print_array

print_next:
	lw $a0, 0($t0)			# Load next value
	li $v0, 1			# Print integer syscall
	syscall

	addi $t2, $t2, 1		# Increment counter
	blt $t2, $t1, print_comma	# Print comma if not last value
	j print_loop			# Otherwise, continue loop

print_comma:
	li $v0, 4			# Print string syscall
	la $a0, comma			# Load address of comma
	syscall
	addi $t0, $t0, 4		# Move to next integer in array
	j print_loop			# Continue loop

finish_print_array:
	li $v0, 4			# Print string syscall
	la $a0, evenSumMsg		# Load address of evenSumMsg
	syscall

print_sum:
	li $v0, 1			# Print integer syscall
	move $a0, $t3			# Load sum of even values
	syscall

	li $v0, 4			# Print string syscall
	la $a0, newline			# Load address of newline
	syscall

	li $v0, 10			# Gracefully finish the execution of the program with the "exit" syscall
	syscall
