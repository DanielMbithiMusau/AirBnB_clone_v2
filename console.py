#!/usr/bin/env python3
"""Shell console for the application"""
import cmd
import shlex
from models.base_model import BaseModel
from models import storage
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class HBNBCommand(cmd.Cmd):
    """Command interpreters for HBNB."""
    prompt = '(hbnb) '

    def do_create(self, arg):
        """Creates a new instance of BaseModel, saves it and prints the id.

        Usage: create <class name>
        """
        if not arg:
            print("** class name missing **")
            return

        print(arg)
        class_name, *params = arg.split()
        print(class_name)
        print(params)
        attrs = {}

        for param in params:
            key, value = param.split('=')

            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace('_', ' ').replace('\\"', '"')
            elif '.' in value:
                try:
                    value = float(value)
                except ValueError:
                    continue
            else:
                try:
                    value = int(value)
                except ValueError:
                    continue

            attrs[key] = value

        try:
            obj = eval(class_name)(**attrs)
            obj.save()
            print(obj.id)

        except NameError:
            print("** class doesn't exist **")
            return

    def do_show(self, arg):
        """Prints the string representation of an instance based on the class
        name and id.

        Usage: show <class name> <class id>
        """
        args = arg.split()
        if not args:
            print("** class name missing **")
            return
        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return
        if len(args) < 2:
            print("** instance id missing **")
            return
        objs = storage.all()
        key = f"{args[0]}.{args[1]}"
        if key not in objs:
            print("** no instance found **")
            return
        print(objs[key])

    def do_destroy(self, arg):
        """Deletes an instance based on the class name and id.

        Usage: destroy <class name> <class id>
        """
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return

        objs = storage.all()
        key = f"{args[0]}.{args[1]}"
        if key not in objs:
            print("** no instance found **")
            return

        del objs[key]
        storage.save()

    def do_all(self, arg):
        """Prints all string representation of all instances based
        or not on the class name.

        Usage: all <class name> or all <.>
        """
        if not arg:
            print("** class name missing **")
            return

        if arg == '.':
            objs = storage.all()
        else:
            try:
                cls = eval(arg)
                objs = storage.all(cls)
            except NameError:
                print("** class doesn't exist **")
                return
        for obj_id in objs.keys():
            obj = objs[obj_id]
            print(obj)

    def do_update(self, arg):
        """Updates an instance based on the class name and id by
        adding or updating attribute.

        Usage: update <class name> <id> <attribute name> "<attribute value>"
        """
        args = arg.split()

        if not args:
            print("** class name missing **")
            return

        try:
            cls = eval(args[0])
        except NameError:
            print("** class doesn't exist **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return
        objs = storage.all()
        key = f"{args[0]}.{args[1]}"
        if key not in objs:
            print("** no instance found **")
            return

        if len(args) < 3:
            print("** attribute name missing **")
            return

        if len(args) < 4:
            print("** value missing **")
            return

        obj = objs[key]
        attr_name = args[2]
        attr_value = args[3]

        setattr(obj, attr_name, attr_value)

    def do_quit(self, line):
        """Quit command to exit the program.

        Usage: quit
        """
        return True

    def default(self, line):
        """Handle default behavior for command not recognized."""
        args = line.split(".")
        cls_name = args[0]
        command = args[1].split("(")[0]
        try:
            cls = eval(cls_name)
        except NameError:
            print("** class doesn't exist **")
            return
        if command == "all":
            objs = storage.all(cls)
            for obj_id in objs.keys():
                obj = objs[obj_id]
                print(obj)
            return
        elif command == "count":
            print(storage.count(cls))
            return
        elif command == "show":
            if len(args[1]) > 4:
                id_str = args[1].split("(")[1].split(")")[0]
                obj_id = id_str.strip("\"'")
                key = f"{cls_name}.{obj_id}"
                if key in storage.all():
                    print(storage.all()[key])
                    return
            print("** no instance found **")
            return
        elif command == "destroy":
            if len(args[1]) > 4:
                id_str = args[1].split("(")[1].split(")")[0]
                obj_id = id_str.strip("\"'")
                key = f"{cls_name}.{obj_id}"
                objs = storage.all()

                if key not in objs:
                    print("** no instance found **")
                    return
                del objs[key]
                storage.save()
                return
        elif command == "update":
            if len(args[1]) > 4:
                if len(args) < 2:
                    print("** instance id missing **")
                    return
                arg_list = shlex.split(args[1][:-1])

                if len(arg_list) < 2:
                    print("** attribute name missing **")
                    return
                if len(arg_list) < 3:
                    print("** value missing **")
                    return

                obj_id = arg_list[0].replace("update", '') \
                                    .replace('(', '') \
                                    .replace('"', '') \
                                    .replace(',', '')
                attr_name = arg_list[1].replace(',', '')
                attr_val = arg_list[2].strip("\"'")

                key = f"{cls_name}.{obj_id}"
                objs = storage.all()

                if key not in objs:
                    print("** no instance found **")
                    return

                obj = objs[key]

                if isinstance(arg_list[1], dict):
                    for key, value in arg_list[1].items():
                        setattr(obj, key, value)
                else:
                    setattr(obj, attr_name, attr_val)
                obj.save()

        else:
            print(f"** Unknown syntax: {line} **")

    def do_EOF(self, line):
        """exit the program with EOF."""
        print()
        return True

    def emptyline(self):
        """Empty line does nothing."""
        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
