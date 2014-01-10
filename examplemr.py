# A mapper function takes one argument, and maps it to something else.
def mapper(item):
    # This example mapper turns the input lines into integers
    return int(item)

# A reducer function takes two arguments, and reduces them to one.
# The first argument is the current accumulated value, which starts
# out with the value of the first element.
def reducer(accum, item):
    # This example reducer sums the values
    return accum+item


# You'd run this via the following command:
#
#   some_input_cmd | ./pythonmr.py --auto=examplemr | some_output_command
#
# or...
#
#   ./pythonmr.py --in=infile.txt --out=outfile.txt --auto=examplemr
