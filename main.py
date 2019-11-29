"""Main entrypoint for the dictionary app."""
import controller


def main():
    c = controller.Controller('t/test.json')
    c.add_entry('chico', 'ragazzo')
    c.add_entry('manzana', 'mela')
    print(c.search_entries())
    print(c.search_entries('manana', 0.6))


if __name__ == '__main__':
    main()
