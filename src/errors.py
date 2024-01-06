# Color codes
RED = "\u001b[31m"
RESET = "\u001b[0m"
# ^^ MORE COLORS:
#  https://www.lihaoyi.com/post/BuildyourownCommandLinewithANSIescapecodes.html


def error(message, loc=None):
    # TODO: You should use the location to
    #        print the line where an error occurs

    print(RED, message, RESET, sep="")
    exit(1)
