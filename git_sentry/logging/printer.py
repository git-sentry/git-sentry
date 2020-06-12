import click


def error_out(error_message):
    return click.style(error_message, fg='red')


def focus_out(focus_message):
    return click.style(focus_message, fg='cyan')


def write(text, indent=0):
    click.echo(f'{pad(text, indent)}')


def pad(text, indent=0):
    prefix = ''.join(['   '] * indent)
    return f'{prefix}{text}'


def section(header):
    pre = '-' * 20 + f' {header} '
    remaining_length = 80 - len(pre)
    return f"{pre}{'-' * remaining_length}"
