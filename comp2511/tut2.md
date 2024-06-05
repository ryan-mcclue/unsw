<!-- SPDX-License-Identifier: zlib-acknowledgement -->
Default init values of 0, null for classes

Want to handle various cases, e.g. another constructor for when can be null etc.
Only have getters/setters if need to be used from a 'behaviourally' point of view

equals(Object o)
{
  return super.equals(o) && something.equals();
}


