# QueryController
A tool that puts you in full control of query strings.

## **pt-br:**
QueryController, é uma ferramenta que tem por objetivo
trocar os valores de cara parâmetro de uma lista de URLs para um determinado valor. (ex: 'W00t').
A grande diferença entre as outras ferramentas que encontrei pelo github, é conseguir substituir
um parâmetro por vez ou até mesmo ter o controle de quais parâmetros você quer substituir o valor.

Uma coisa que identifiquei nas ferramentas existentes foi que todas elas substituiam todos os valores
dos parâmetro de uma única vez e isso dependendo da aplicação pode quebrar o fluxo.

## **en:**
QueryController is a tool that aims to replace the values of each parameter from a list of URLs with a specific value (e.g. 'W00t').
The big difference between this tool and others I found on GitHub is that it can replace one parameter at a time or 
even allow you to control which parameters you want to replace the value for.

One thing I noticed about existing tools is that they all replace all parameter values at once, 
which, depending on the application, can break the flow.

## Example
Input file:
```r
$ cat target.txt
https://www.example.com/card/?pid=site&c=home&af_js_web=true&af_ad=faca-parte&af_sub1=site
https://www.example.com/termos-uso/assets/css/styles.css?d=1675276902567
https://www.example.com/termos-uso/assets/js/scripts.js?d=1675276902567
```
>By default the tool will ignore `.js` and `.css` extensions.

### Replace all params value
```r
$ python3 QueryController.py -f target.txt
https://www.example.com/card/?pid=W00t&c=home&af_js_web=true&af_ad=faca-parte&af_sub1=site
https://www.example.com/card/?pid=site&c=W00t&af_js_web=true&af_ad=faca-parte&af_sub1=site
https://www.example.com/card/?pid=site&c=home&af_js_web=W00t&af_ad=faca-parte&af_sub1=site
https://www.example.com/card/?pid=site&c=home&af_js_web=true&af_ad=W00t&af_sub1=site
https://www.example.com/card/?pid=site&c=home&af_js_web=true&af_ad=faca-parte&af_sub1=W00t
```
### Filter specified params
Input file:
```r
$ cat params.txt
pid
af_ad
af_sub1
```
Output:
```r
$ python3 QueryController.py -f target.txt -q params.txt
https://www.example.com/card/?pid=W00t&c=home&af_js_web=true&af_ad=faca-parte&af_sub1=site
https://www.example.com/card/?pid=site&c=home&af_js_web=true&af_ad=W00t&af_sub1=site
https://www.example.com/card/?pid=site&c=home&af_js_web=true&af_ad=faca-parte&af_sub1=W00t
```


## Similar tools I've found:

* [ParamChanger](https://github.com/mathis2001/ParamChanger)
* [ParamReplace](https://github.com/Phoenix1112/ParamReplace)
* [qsreplace](https://github.com/tomnomnom/qsreplace)

## To-Do List:
- [x] Filter only specified params.
- [x] Change all params one at time.
- [ ] possibility to avoid some extensions .css, .png, etc...
- [ ] Receive input from a piped stdin.
- [ ] Add top payloads list.
