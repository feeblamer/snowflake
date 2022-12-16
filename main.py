from strategy import Context, SnowflakeTurtle


def main():
    snowflake = SnowflakeTurtle(8, 30, 300, name_shape='third shape')
    ctx = Context(snowflake)
    ctx.draw_snowflake()


if __name__ == "__main__":
    main()
