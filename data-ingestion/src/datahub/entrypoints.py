from pyspark.sql import SparkSession
from pyspark.sql.functions import col
# import datahub
from datahub.mysql import check_from_table
import sys
import click
import datahub as datahub_package
import click_spinner
from typing import Optional
def main(**kwargs):
    # print("This is the Nuodata Goverance CLI")
    try:
        sys.exit(nt(standalone_mode=False, **kwargs))
    except click.Abort:
        # Click already automatically prints an abort message, so we can just exit.
        sys.exit(1)
    except click.ClickException as error:
        error.show()
        sys.exit(1)
    except Exception as exc:
        print(exc)
        # if not should_show_stack_trace(exc):
        #     # Don't print the full stack trace for simple config errors.
        #     logger.debug("Error: %s", exc, exc_info=exc)
        #     click.secho(f"{exc}", fg="red")
        # else:
        #     logger.exception(f"Command failed: {exc}")

        # logger.debug(
        #     f"DataHub CLI version: {datahub_package.__version__} at {datahub_package.__file__}"
        # )
        # logger.debug(
        #     f"Python version: {sys.version} at {sys.executable} on {platform.platform()}"
        # )
        # gms_config = get_gms_config()
        # if gms_config:
        #     logger.debug(f"GMS config {gms_config}")
        print("inside exception")
        sys.exit(1)


@click.group(
    context_settings=dict(
        # Avoid truncation of help text.
        # See https://github.com/pallets/click/issues/486.
        max_content_width=120,
    ),
)

@click.option(
    "--platform",
    type=str,
    help="the platform from which to ingest data.",
)

@click.pass_context
def nt(
        ctx: click.Context,
        platform,
        # debug: bool,
        # log_file: Optional[str],
        # debug_vars: bool,
        # detect_memory_leaks: bool,
) -> None:
    # if debug_vars:
    #     # debug_vars implies debug. This option isn't actually used here, but instead
    #     # read directly from the command line arguments in the main entrypoint.
    #     debug = True
    #
    # debug = debug or get_boolean_env_variable("DATAHUB_DEBUG", False)

    # Note that we're purposely leaking the context manager here.
    # Technically we should wrap this with ctx.with_resource(). However, we have
    # some important error logging in the main() wrapper function that we don't
    # want to miss. If we wrap this with ctx.with_resource(), then click would
    # clean it up before those error handlers are processed.
    # So why is this ok? Because we're leaking a context manager, this will
    # still get cleaned up automatically when the memory is reclaimed, which is
    # worse-case at program exit.
    # global _logging_configured
    # _logging_configured = None  # see if we can force python to GC this
    # _logging_configured = configure_logging(debug=debug, log_file=log_file)
    # _logging_configured.__enter__()

    # Setup the context for the memory_leak_detector decorator.
    ctx.ensure_object(dict)
    ctx.obj["platform"] = platform

@nt.command()
def version() -> None:
    # print('Im here!!!!')
    # click.echo("NT test Command!")
    click.echo(f"Nuodata Ingestion version: {datahub_package.nice_version_name()}")

@nt.command()
@click.pass_context
def ingest(ctx) -> None:
    click.echo("Initiating ingestion process")
    click.echo(ctx.obj['platform'])
    import time
    with click_spinner.spinner(disable=False):
        click.echo("Ingestion process would start here..")
        # time.sleep(5)
        # click.echo("Still working on it...")
        check_from_table(ctx.obj['platform'])
    click.echo("Ingestion process complete")