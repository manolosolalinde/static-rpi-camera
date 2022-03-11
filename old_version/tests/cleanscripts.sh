#!/bin/bash
FILES=*.sh
for filename in $FILES; do
   sed -ri 's:^M$::' ${filename};
   sed -i -e 's/\r$/\n/' ${filename};
done