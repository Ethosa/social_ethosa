# -*- coding; utf-8 -*-
# author: Ethosa

# we import the functionality we need
from social_ethosa import Keyboard, Button, __version__ as seVersion

# Let's create a single button
my_first_button = Button("text", label="Hello world :)")

# Initialize the inline keyboard
keyboard = Keyboard(inline=True)

# Add this button to it several times
keyboard.addButton(my_first_button)
keyboard.addButton(my_first_button)
keyboard.addButton(my_first_button)
# Note that the addLine() method is optional
# because the keyboard automatically jumps to a new line if necessary.
keyboard.addButton(my_first_button)
keyboard.addButton(my_first_button)
keyboard.addButton(my_first_button)

keyboard.addButton(my_first_button)
keyboard.addButton(my_first_button)
keyboard.addButton(my_first_button)

# draw a keyboard in the console
keyboard.visualize()

# we get a compiled keyboard
compiled = keyboard.compile()

# Displaying the compiled version
print(compiled)

# get the version of the library itself
print("\nversion", seVersion)
