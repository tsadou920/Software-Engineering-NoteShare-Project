# Why do we use the class Meta inside the ModelForm in Django? [(source)](https://www.quora.com/Why-do-we-use-the-class-Meta-inside-the-ModelForm-in-Django)

Your question can be interpreted in two ways:

1. For what purpose inner `Meta` class is used?
2. Why inner `Meta`  class is used to solve the problem it solves (which is defining  metadata)? What can’t the metadata be simply defined as attributes?

First, I’ll explain the answer the first question.

`Meta` class is simply an [inner class](https://pythonspot.com/en/inner-classes/). In Django, the use of `Meta` class is simply to provide **metadata** to the `ModelForm` class. It is different from [metaclass](http://stackoverflow.com/questions/100003/what-is-a-metaclass-in-python) of a Class in Python.

So what exactly is **metadata** in case of a `ModelForm`?

Any information that is “not a form `Field`”  can be considered as metadata. Django provides sensible defaults to all  fields. But if you want to override the default behavior of fields, you  can define the corresponding meta options. Some meta options are  compulsory.

For example:

- `model`: Model class to use for creating Form
- `fields`: list to fields to include in the Form
- `exclude`: list of fields to exclude from the Form
- `widgets`: a dictionary of field-widget pairs

And so on, there are many more meta options you can define inside Meta class.

Now to second question. Why `Meta` class is used to define the meta information? Why not simply define them as class attributes?

It was more of a design decision to use `Meta`.  You can access the contents of inner class from Outer class. It  provides a cleaner API and keeps fields (which are the crux of any form)  and the form configuration options separate.

In general, inner class are avoided in Python and they don’t provide any huge advantage but do cause some minor inconveniences.