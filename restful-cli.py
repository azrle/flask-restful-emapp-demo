#!/usr/bin/env python
import click
import requests
import json
import os


@click.group()
@click.option('--endpoint', default='http://localhost:5000/api',
              help='base endpoint of API')
@click.option('--api-key', default=os.getenv('EMAPP_API_KEY', ''),
              help='API key token')
@click.pass_context
def cli(ctx, endpoint, api_key):
    ctx.ensure_object(dict)
    ctx.obj['ENDPOINT'] = endpoint
    ctx.obj['API_KEY'] = api_key


@cli.command()
@click.pass_context
def list_events(ctx):
    r = requests.get(url='{}/events'.format(ctx.obj['ENDPOINT']),
                     headers={'x-simple-auth': ctx.obj['API_KEY']})
    if r.ok:
        click.echo(json.dumps(r.json(), indent=4, sort_keys=True))
    else:
        click.echo('Error status: {}'.format(r.status_code), err=True)
        click.echo(r.text, err=True)


@cli.command()
@click.option('--event-id', prompt='Event ID', type=int,
              help='event_id to signup for')
@click.option('--email', prompt='Email',
              help='email used to sign up')
@click.pass_context
def signup(ctx, event_id, email):
    r = requests.post(url='{}/signup/events/{}/email/{}'.format(
        ctx.obj['ENDPOINT'], event_id, email),
        headers={'x-simple-auth': ctx.obj['API_KEY']})
    if r.ok:
        click.echo('Succeeded to sign up for the event.')
    else:
        click.echo('Error status: {}'.format(r.status_code), err=True)
        click.echo(r.text, err=True)


@cli.command()
@click.option('--event-id', prompt='Event ID', type=int,
              help='event_id to remove signup from')
@click.option('--email', prompt='Email',
              help='email to remove')
@click.pass_context
def remove_signup(ctx, event_id, email):
    r = requests.delete(url='{}/signup/events/{}/email/{}'.format(
        ctx.obj['ENDPOINT'], event_id, email),
        headers={'x-simple-auth': ctx.obj['API_KEY']})
    if r.ok:
        click.echo('Succeeded to remove signup from the event.')
    else:
        click.echo('Error status: {}'.format(r.status_code), err=True)
        click.echo(r.text, err=True)


@cli.command()
@click.option('--event-id', prompt='Event ID', type=int,
              help='event_id to list signup emails')
@click.pass_context
def list_signup(ctx, event_id):
    r = requests.get(url='{}/signup/events/{}'.format(
        ctx.obj['ENDPOINT'], event_id),
        headers={'x-simple-auth': ctx.obj['API_KEY']})
    if r.ok:
        click.echo(json.dumps(r.json(), indent=4, sort_keys=True))
    else:
        click.echo('Error status: {}'.format(r.status_code), err=True)
        click.echo(r.text, err=True)


if __name__ == '__main__':
    cli(obj={})
