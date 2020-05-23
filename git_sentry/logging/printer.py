import click


def error_out(error_message):
    return click.style(error_message, fg='red')


def focus_out(focus_message):
    return click.style(focus_message, fg='cyan')


def write(text, indent=0):
    indent = ''.join(['\t'] * indent)
    click.echo(f'{indent}{text}')