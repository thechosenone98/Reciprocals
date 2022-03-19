import click

@click.command()
@click.argument("number")
@click.option("--n", help="The number of digits of precision that is desired")
@click.option("--o", help="The outputfile in which to save the result")
@click.option("--m", is_flag=True, help="Mark all the periods with |")
@click.option("--p", is_flag=True, help="Also print the period of the number")
def reciprocal(number, n, m, p, o):
    """Takes the reciprocal of any number up to N digits"""
    number = int(number)
    n = int(n)
    reciprocal = ["0"]
    remainder_set = set()
    period = 0
    first_period = True
    if number == 0:
        click.echo(click.style("Can't take the reciprocal of zero!", fg="red"))
    else:
        # Calculates the reciprocal up to N digits
        rem = 1
        # Do an extra digit for the rounding later
        counter = n + 2
        while counter > 0:
            if first_period and rem in remainder_set:
                first_period = False
                period = (n + 2) - counter
            remainder_set.add(rem)
            if rem == 0:
                break
            while True:
                if rem < number:
                    rem *= 10
                    if rem < number:
                        reciprocal.append("0")
                        counter -= 1
                else:
                    break
            digit = rem // number
            rem -= number * digit
            reciprocal.append(str(digit))
            counter -= 1
        reciprocal.insert(1, '.')
        # Trim to correct lenght (algorithm above may compute two or more digit at a time resulting in incorrect number of digits)
        # The +3 is to include 0. and the leading rounding digit
        if len(reciprocal) > n + 3:
            reciprocal = reciprocal[:n+3]
        # Rounding
        if int(reciprocal[-1]) >= 5:
            reciprocal[-2] = str(int(reciprocal[-2]) + 1)
        # Remove last digit
        reciprocal.pop()
        # Insert period marker if the marker option is set
        if m:
            # Skip the initial 0.
            count = period + 2
            while count < len(reciprocal):
                reciprocal.insert(count, '|')
                count += period + 1
        click.echo(f"Reciprocal of {number} is:\n{''.join(reciprocal)}")
        if p:
            click.echo(f"Period of 1/{number} is {period}")
        # Save to output file
        if o:
            with open(o, "w") as outputfile:
                outputfile.write(''.join(reciprocal))
            click.echo("Saved successfully!")


if __name__ == "__main__":
    reciprocal()