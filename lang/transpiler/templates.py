from string import Template as t

WRAPPER_TPL = t("""
package main

func main(){
    $body
}

""")


FN_CALL_TPL = t("""
$name($args)
""")

