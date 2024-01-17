#!/usr/bin/python3
"""This is the console for AirBnB"""
import cmd
from datetime import datetime
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from shlex import split
from models import storage


class HBNBCommand(cmd.Cmd):
    """this class is entry point of the command interpreter
    """
    prompt = "(hbnb) "
    __classes = {"BaseModel", "User", "City", "State", "Amenity", "Place",
                 "Review"}

    def emptyline(self):
        """
        this wil ignores empty spaces
        """
        pass

    def _quit(self, line):
        """
        this will quit command to exit the program
        """
        return True

    def _EOF(self, line):
        """
        this is quit command to exit the program at end of file
        """
        print("")
        return True

    def _create(self, line):
        """
        this will Creates a new instance of BaseModel and saves
        """
        try:
            if not line:
                raise SyntaxError()
            _list = line.split(" ")

            kwargs = {}
            for d in range(1, len(_list)):
                key, val = tuple(_list[d].split("="))
                if val[0] == '"':
                    val = val.strip('"').replace("_", " ")
                else:
                    try:
                        val = eval(val)
                    except (SyntaxError, NameError):
                        continue
                kwargs[key] = val

            if kwargs == {}:
                obj = eval(_list[0])()
            else:
                obj = eval(_list[0])(**kwargs)
                storage.new(obj)
            print(obj.id)
            obj.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def _show(self, line):
        """this will Print string representation of an instance
        Exceptions:
            SyntaxError: if no args given
            KeyError: if no valid id given
            NameError: if no object taht has the name
            IndexError: if no id given
        """
        try:
            if not line:
                raise SyntaxError()
            _list = line.split(" ")
            if _list[0] not in self.__classes:
                raise NameError()
            if len(_list) < 2:
                raise IndexError()
            obje = storage.all()
            key = _list[0] + '.' + _list[1]
            if key in obje:
                print(obje[key])
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def _destroy(self, line):
        """this will remove instance based on the class name and id
        Exceptions:
            SyntaxError: if no args given
            NameError:if no object taht has the name
            IndexError: if no id given
            KeyError: if no valid id given
        """
        try:
            if not line:
                raise SyntaxError()
            _list = line.split(" ")
            if _list[0] not in self.__classes:
                raise NameError()
            if len(_list) < 2:
                raise IndexError()
            obje = storage.all()
            key = _list[0] + '.' + _list[1]
            if key in obje:
                del obje[key]
                storage.save()
            else:
                raise KeyError()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")

    def _all(self, line):
        """
        this will prints all string representation of all instances
        Exceptions:
            NameError: if no object taht has the name
        """
        """objects = storage.all()
        my_list = []"""

        if not line:
            obj = storage.all()
            print([obj[key].__str__() for key in obj])
            return
        try:
            args = line.split(" ")
            if args[0] not in self.__classes:
                raise NameError()

            obj = storage.all(eval(args[0]))
            print([obj[key].__str__() for key in obj])

        except NameError:
            print("** class doesn't exist **")

    def _update(self, line):
        """
        this updates an instanceby adding or updating attribute
        Exceptions:
            SyntaxError: when no args giv
            KeyError: when no valid id given
            AttributeError: when no attribute given
            NameError: when no object taht has the name
            IndexError: when no id given
            ValueError: if no value given
        """
        try:
            if not line:
                raise SyntaxError()
            _list = split(line, " ")
            if _list[0] not in self.__classes:
                raise NameError()
            if len(_list) < 2:
                raise IndexError()
            obje = storage.all()
            key = _list[0] + '.' + _list[1]
            if key not in obje:
                raise KeyError()
            if len(_list) < 3:
                raise AttributeError()
            if len(_list) < 4:
                raise ValueError()
            v = obje[key]
            try:
                v.__dict__[_list[2]] = eval(_list[3])
            except Exception:
                v.__dict__[_list[2]] = _list[3]
                v.save()
        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")
        except IndexError:
            print("** instance id missing **")
        except KeyError:
            print("** no instance found **")
        except AttributeError:
            print("** attribute name missing **")
        except ValueError:
            print("** value missing **")

    def count(self, line):
        """
        this will count the occurance of instances of a class
        """
        counter = 0
        try:
            _list = split(line, " ")
            if _list[0] not in self.__classes:
                raise NameError()
            obje = storage.all()
            for key in obje:
                name = key.split('.')
                if name[0] == _list[0]:
                    counter += 1
            print(counter)
        except NameError:
            print("** class doesn't exist **")

    def strip_clean(self, args):
        """
        this willstrips the argument and return a string of command
        """
        nw_list = []
        nw_list.append(args[0])
        try:
            mi_dict = eval(
                args[1][args[1].find('{'):args[1].find('}')+1])
        except Exception:
            mi_dict = None
        if isinstance(mi_dict, dict):
            nw_str = args[1][args[1].find('(')+1:args[1].find(')')]
            nw_list.append(((nw_str.split(", "))[0]).strip('"'))
            nw_list.append(mi_dict)
            return nw_list
        nw_str = args[1][args[1].find('(')+1:args[1].find(')')]
        nw_list.append(" ".join(nw_str.split(", ")))
        return " ".join(i for i in nw_list)

    def default(self, line):
        """
        this will retrieve and restore all instances of a class and
        retrieve the number of instances
        """
        _list = line.split('.')
        if len(_list) >= 2:
            if _list[1] == "all()":
                self._all(_list[0])
            elif _list[1] == "count()":
                self.count(_list[0])
            elif _list[1][:4] == "show":
                self._show(self.strip_clean(_list))
            elif _list[1][:7] == "destroy":
                self._destroy(self.strip_clean(_list))
            elif _list[1][:6] == "update":
                args = self.strip_clean(_list)
                if isinstance(args, list):
                    obj = storage.all()
                    key = args[0] + ' ' + args[1]
                    for k, v in args[2].items():
                        self._update(key + ' "{}" "{}"'.format(k, v))
                else:
                    self._update(args)
        else:
            cmd.Cmd.default(self, line)

if __name__ == '__main__':
    HBNBCommand().cmdloop()
