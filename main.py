"""Main entrypoint for the dictionary app."""
import controller


def main():
    c = controller.Controller('t/test.json')
    c.save()


if __name__ == '__main__':
    main()
