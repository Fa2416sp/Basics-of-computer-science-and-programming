#ifndef RAT_IO_H
#define RAT_IO_H

#include "rational.h"

void rat_print(rational_t r);
rational_t rat_parse(const char *str);

#endif
