# -*- coding: utf-8 -*-
from base import *
from flask import Flask, session, g, render_template, url_for, request, redirect, make_response, abort

from sage.all import *
import tempfile, os
import pymongo
from Lfunction import *
import LfunctionComp
import LfunctionPlot
from utils import to_dict, make_logger
import bson
from Lfunctionutilities import lfuncDStex, lfuncEPtex, lfuncFEtex

logger = make_logger("LF")

##import upload2Db.py


###########################################################################
#   Route functions
###########################################################################

@app.route("/L/")
@app.route("/L/<arg1>/") # arg1 is EllipticCurve, ModularForm, Character, etc
@app.route("/L/<arg1>/<arg2>/") # arg2 is field
@app.route("/L/<arg1>/<arg2>/<arg3>/") #arg3 is label
@app.route("/L/<arg1>/<arg2>/<arg3>/<arg4>/")
@app.route("/L/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/")
@app.route("/L/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/")
@app.route("/L/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/")
@app.route("/L/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/<arg8>/")
@app.route("/L/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/<arg8>/<arg9>/")
def render_Lfunction(arg1 = None, arg2 = None, arg3 = None, arg4 = None, arg5 = None, arg6 = None, arg7 = None, arg8 = None, arg9 = None):
    return render_webpage(request, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9)

@app.route("/Lfunction/")
@app.route("/Lfunction/<arg1>/")
@app.route("/Lfunction/<arg1>/<arg2>/")
@app.route("/Lfunction/<arg1>/<arg2>/<arg3>/")
@app.route("/Lfunction/<arg1>/<arg2>/<arg3>/<arg4>/")
@app.route("/Lfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/")
@app.route("/Lfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/")
@app.route("/Lfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/")
@app.route("/Lfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/<arg8>/")
@app.route("/Lfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/<arg8>/<arg9>/")
@app.route("/L-function/")
@app.route("/L-function/<arg1>/")
@app.route("/L-function/<arg1>/<arg2>/")
@app.route("/L-function/<arg1>/<arg2>/<arg3>/")
@app.route("/L-function/<arg1>/<arg2>/<arg3>/<arg4>/")
@app.route("/L-function/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/")
@app.route("/L-function/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/")
@app.route("/L-function/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/")
@app.route("/L-function/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/<arg8>/")
@app.route("/L-function/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/<arg8>/<arg9>/")
def render_Lfunction_redirect(**args):
    args.update(request.args)
    return redirect(url_for("render_Lfunction", **args), code=301)

@app.route("/plotLfunction/")
@app.route("/plotLfunction/<arg1>/")
@app.route("/plotLfunction/<arg1>/<arg2>/")
@app.route("/plotLfunction/<arg1>/<arg2>/<arg3>/")
@app.route("/plotLfunction/<arg1>/<arg2>/<arg3>/<arg4>/")
@app.route("/plotLfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/")
@app.route("/plotLfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/")
@app.route("/plotLfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/")
@app.route("/plotLfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/<arg8>/")
@app.route("/plotLfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/<arg8>/<arg9>/")
def plotLfunction(arg1 = None, arg2 = None, arg3 = None, arg4 = None, arg5 = None, arg6 = None, arg7 = None, arg8 = None, arg9 = None):
    return render_plotLfunction(request, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9)

@app.route("/zeroesLfunction/")
@app.route("/zeroesLfunction/<arg1>/")
@app.route("/zeroesLfunction/<arg1>/<arg2>/")
@app.route("/zeroesLfunction/<arg1>/<arg2>/<arg3>/")
@app.route("/zeroesLfunction/<arg1>/<arg2>/<arg3>/<arg4>/")
@app.route("/zeroesLfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/")
@app.route("/zeroesLfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/")
@app.route("/zeroesLfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/")
@app.route("/zeroesLfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/<arg8>/")
@app.route("/zeroesLfunction/<arg1>/<arg2>/<arg3>/<arg4>/<arg5>/<arg6>/<arg7>/<arg8>/<arg9>/")
def zeroesLfunction(arg1 = None, arg2 = None, arg3 = None, arg4 = None, arg5 = None, arg6 = None, arg7 = None, arg8 = None, arg9 = None):
    return render_zeroesLfunction(request, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9)

@app.route("/browseGraph/")
def browseGraph():
    return render_browseGraph(request.args)

@app.route("/browseGraphTMP/")
def browseGraphTMP():
    return render_browseGraphTMP(request.args)

@app.route("/browseGraphHolo/")
def browseGraphHolo():
    return render_browseGraphHolo(request.args)

@app.route("/browseGraphChar/")
def browseGraphChar():
    return render_browseGraphHolo(request.args)


###########################################################################
#   Functions for rendering the web pages
###########################################################################

def render_webpage(request, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9):
    args = request.args
    temp_args = to_dict(args)
    
    if len(args) == 0:  #This ensures it's a navigation page 
        if not arg1: # this means we're at the start page
            info = set_info_for_start_page()
            return render_template("LfunctionNavigate.html", **info)
        
        elif arg1.startswith("degree"):
            degree = int(arg1[6:])
            info = { "degree" : degree }
            info["key"] = 777
            info["bread"] =  [('L-functions', url_for("render_Lfunction")), ('Degree '+str(degree), url_for('render_Lfunction', arg1=str(degree)))]
            if degree == 1:
                info["contents"] = [LfunctionPlot.getOneGraphHtmlChar(1,35,1,13)]
                info['friends'] = [('Dirichlet Characters', url_for('render_Character'))]
            elif degree == 2:
                info["contents"] = [processEllipticCurveNavigation(11,65), LfunctionPlot.getOneGraphHtmlHolo(1, 6, 2, 14),
                                    processMaassNavigation()]
            elif degree == 3 or degree == 4:
                info["contents"] = LfunctionPlot.getAllMaassGraphHtml(degree)
                
            return render_template("DegreeNavigateL.html", title = 'Degree ' + str(degree)+ ' L-functions', **info)
            
        elif arg1 == 'custom': # need a better name
            return "not yet implemented"
        
    try:
      L = generateLfunctionFromUrl(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, temp_args)
    except Exception as e:
      # throw exception if not UserError
      if len(e.args) > 1 and e.args[1] != 'UserError': raise
      info = { 'content': 'Sorry, there has been a problem: %s' % e.args[0], 'title': 'Error' }
      return render_template('LfunctionSimple.html', info=info, **info), 500
   
    try:
        logger.info(temp_args)
        if temp_args['download'] == 'lcalcfile':
            return render_lcalcfile(L, request.url)
    except:
        pass #Do nothing

    info = initLfunction(L, temp_args, request)

    return render_template('Lfunction.html', **info)
    

def generateLfunctionFromUrl(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, temp_args):
    if (arg1 == 'Riemann' or (arg1 == 'Character' and arg2 == 'Dirichlet' and arg3 == '1' and arg4 == '0')
        or (arg1 == 'NumberField' and arg2 == '1.1.1.1')):
        return RiemannZeta()

    elif arg1 == 'Character' and arg2 == 'Dirichlet':
        return Lfunction_Dirichlet( charactermodulus = arg3, characternumber = arg4)

    elif arg1 == 'EllipticCurve' and arg2 == 'Q':
        return Lfunction_EC( label = arg3)

    elif arg1 == 'ModularForm' and arg2 == 'GL2' and arg3 == 'Q' and arg4 == 'holomorphic': # this has args: one for weight and one for level
        logger.info(arg5+arg6+str(arg7)+str(arg8)+str(arg9))
        return Lfunction_EMF( level = arg5, weight = arg6, character = arg7, label = arg8, number = arg9)

    elif arg1 == 'ModularForm' and arg2 == 'GL2'and arg3 == 'Q' and arg4 == 'Maass':
        logger.info(db)
        return Lfunction_Maass(dbid = bson.objectid.ObjectId(arg5), dbName = 'MaassWaveForm', dbColl = temp_args['db'])
    
    elif arg1 == 'ModularForm' and (arg2 == 'GSp4' or arg2 == 'GL4' or  arg2 == 'GL3') and arg3 == 'Q' and arg4 == 'maass':
        return Lfunction_Maass( dbid = arg5, dbName = 'Lfunction', dbColl = 'LemurellMaassHighDegree')

    elif arg1 == 'NumberField':
        return DedekindZeta( label = str(arg2))

    elif arg1 == 'Lcalcurl':
        return Lfunction( Ltype = arg1, url = arg2)
    
    raise Exception("Not Found")


def set_info_for_start_page():
    ''' Sets the properties of the top L-function page.
    '''
    
    tt = [[{'title':'Riemann','link': url_for('render_Lfunction', arg1='Riemann')},
           {'title':'Dirichlet','link': url_for('render_Lfunction', arg1='degree1') + '#Dirichlet'}],

          [{'title':'Elliptic Curve','link': url_for('render_Lfunction', arg1='degree2') + '#EllipticCurve_Q'},
           {'title':'GL2 Cusp Form', 'link': url_for('render_Lfunction', arg1='degree2') + '#GL2_Q_Holomorphic'},
           {'title':'GL2 Maass Form','link': url_for('render_Lfunction', arg1='degree2') + '#GL2_Q_Maass'}],

          [{'title':'GL3 Maass Form', 'link': url_for('render_Lfunction', arg1='degree3') + '#GL3_Q_Maass'},
           {'title':'GL4 Maass Form', 'link': url_for('render_Lfunction', arg1='degree4') + '#GL4_Q_Maass'},
           {'title':'GSp4 Maass Form', 'link': url_for('render_Lfunction', arg1='degree4') + '#GSp4_Q_Maass'}]]

    info = {
        'degree_list': range(1,5),
        'type_table': tt,
        'type_row_list':[0,1,2] 
    }

    info['title'] = 'L-functions'
    info['bread'] = [('L-functions', url_for("render_Lfunction"))]
#   info['learnmore'] = [('Lmfdb-wiki', 'http://wiki.l-functions.org/L-function')]

    return info
    

def initLfunction(L,args, request):
    info = {'title': L.title}
    info['citation'] = ''
    info['support'] = ''
    info['sv12'] = specialValueString(L, 0.5, '1/2')
    info['sv1'] = specialValueString(L, 1, '1')
    info['args'] = args

    info['credit'] = L.credit
    #info['citation'] = L.citation

    try:
        info['url'] = L.url
    except:
        info['url'] =''

    info['degree'] = int(L.degree)

    info['zeroeslink'] = (request.url.replace('/L/', '/zeroesLfunction/').
                          replace('/Lfunction/', '/zeroesLfunction/').
                          replace('/L-function/', '/zeroesLfunction/') ) #url_for('zeroesLfunction',  **args)

    info['plotlink'] = (request.url.replace('/L/', '/plotLfunction/').
                          replace('/Lfunction/', '/plotLfunction/').
                          replace('/L-function/', '/plotLfunction/') ) #info['plotlink'] = url_for('plotLfunction',  **args)

    info['bread'] = []
    info['properties2'] = set_gaga_properties(L)


    # Create friendlink by removing 'L/' and ending '/'
    friendlink = request.url.replace('/L/','/').replace('/L-function/','/').replace('/Lfunction/','/')
    splitlink = friendlink.rpartition('/')
    friendlink = splitlink[0] + splitlink[2]

    if L.Ltype() == 'maass':
        if L.group == 'GL2':
            minNumberOfCoefficients = 20 # TODO: Fix this to take level into account
            if len(L.dirichlet_coefficients)< minNumberOfCoefficients:
                info['zeroeslink'] = ''
                info['plotlink'] = ''
            info['bread'] = [('L-function','/L') ,('Degree 2',
                              url_for('render_Lfunction', arg1='degree2')),
                             ('\('+L.texname+'\)', request.url )]
            info['friends'] = [('Maass Form ', friendlink)]
        else:
            info['bread'] = [('L-function','/L') ,('Degree ' + str(L.degree),
                             url_for('render_Lfunction', arg1= str(L.degree))), (L.dbid, request.url)]

    elif L.Ltype()  == 'riemann':
        info['bread'] = [('L-function','/L'),('Riemann Zeta',request.url)]
        info['friends'] = [('\(\mathbb Q\)', url_for('by_label', label='1.1.1.1')),  ('Dirichlet Character \(\\chi_{0}\\!\\!\\pmod{1}\)',
                                                                       url_for('render_Character', arg1=1, arg2=0))]

    elif L.Ltype()  == 'dirichlet':
        snum = str(L.characternumber)
        smod = str(L.charactermodulus)
        charname = '\(\\chi_{%s}\\!\\!\\pmod{%s}\)' %(snum,smod)
        info['bread'] = [('L-function','/L'),('Dirichlet Character',url_for('render_Lfunction', arg1='degree1') +'#Dirichlet'),
                         (charname, request.url)]
        info['friends'] = [('Dirichlet Character '+str(charname), friendlink)]
                

    elif L.Ltype()  == 'ellipticcurve':
        label = L.label
        info['friends'] = [('Elliptic Curve', friendlink )]
        info['bread'] = [('L-function','/L'),('Elliptic Curve',url_for('render_Lfunction', arg1='/L/degree2#EllipticCurve_Q')),
                         (label,url_for('render_Lfunction',arg1='EllipticCurve',arg2='Q',arg3= label))]

    elif L.Ltype() == 'ellipticmodularform':
        weight = str(L.weight)
        level = str(L.level)
        character = str(L.character)
        label = str(L.label)
        number = str(L.number)
        info['friends'] = [('Modular Form', friendlink.rpartition('/')[0])] 

    elif L.Ltype() == 'dedekindzeta':
        info['friends'] = [('Number Field', friendlink)]

    elif L.Ltype() in ['lcalcurl', 'lcalcfile']:
        info['bread'] = [('L-function',url_for('render_Lfunction'))]
        

    info['dirichlet'] = lfuncDStex(L, "analytic")
    info['eulerproduct'] = lfuncEPtex(L, "abstract")
    info['functionalequation'] = lfuncFEtex(L, "analytic")
    info['functionalequationSelberg'] = lfuncFEtex(L, "selberg")

    info['learnmore'] = [('L-functions', 'http://wiki.l-functions.org/L-functions') ]
    
    if len(request.args)==0:
        lcalcUrl = request.url + '?download=lcalcfile'
    else:
        lcalcUrl = request.url + '&download=lcalcfile'
        
    info['downloads'] = [('Lcalcfile', lcalcUrl) ]
    
    return info


def set_gaga_properties(L):
    ''' Sets the properties in the properties box in the
        upper right corner
    '''
    ans = [ ('Degree',    str(L.degree))]

    ans.append(('Level',     str(L.level)))
    ans.append(('Sign',      str(L.sign)))

    if L.selfdual:
        sd = 'Self-dual'
    else:
        sd = 'Not self-dual'
    ans.append((None,        sd))

    if L.primitive:
        prim = 'Primitive'
    else:
        prim = 'Not primitive'
#    ans.append((None,        prim))    Disabled until fixed

    return ans


def specialValueString(L, s, sLatex):
    number_of_decimals = 10
    val = L.sageLfunction.value(s)
    lfuncion_value_tex = L.texname.replace('(s', '(' + sLatex)
    return '\(' + lfuncion_value_tex +'\\approx ' + latex(round(val.real(), number_of_decimals)+round(val.imag(), number_of_decimals)*I) + '\)'


def plotLfunction(request, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9):
    pythonL = generateLfunctionFromUrl(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, to_dict(request.args))
    L = pythonL.sageLfunction
    # HSY: I got exceptions that "L.hardy_z_function" doesn't exist
    # SL: Reason, it's not in the distribution of Sage
    if not hasattr(L, "hardy_z_function"):
      return None
    #FIXME there could be a filename collission
    fn = tempfile.mktemp(suffix=".png")
    F=[(i,L.hardy_z_function(CC(.5,i)).real()) for i in srange(-30,30,.1)]
    p = line(F)
    p.save(filename = fn)
    data = file(fn).read()
    os.remove(fn)
    return data

def render_plotLfunction(request, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9):
    data = plotLfunction(request, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9)
    if not data:
        # see note about missing "hardy_z_function" in plotLfunction()
        return redirect(404)
    response = make_response(data)
    response.headers['Content-type'] = 'image/png'
    return response

def render_zeroesLfunction(request, arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9):
    L = generateLfunctionFromUrl(arg1, arg2, arg3, arg4, arg5, arg6, arg7, arg8, arg9, to_dict(request.args))

    if L.degree > 2 or L.Ltype()=="ellipticmodularform"  or L.Ltype()=="maass":  # Too slow to be rigorous here
        search_step = 0.05
        if L.selfdual:
            s = str(L.sageLfunction.find_zeros(-search_step/2 , 20,search_step))
        else:
            s = str(L.sageLfunction.find_zeros(-15,15,search_step))

    else:
        if L.selfdual:
            number_of_zeros = 6
        else:
            number_of_zeros = 8
        s = str(L.sageLfunction.find_zeros_via_N(number_of_zeros, not L.selfdual))

    return s[1:len(s)-1]

def render_browseGraph(args):
    logger.info(args)
    if 'sign' in args:
      data = LfunctionPlot.paintSvgFileAll([[args['group'], int(args['level']), args['sign']]])
    else:
      data = LfunctionPlot.paintSvgFileAll([[args['group'], int(args['level'])]])
    response = make_response(data)
    response.headers['Content-type'] = 'image/svg+xml'
    return response

def render_browseGraphHolo(args):
    logger.info(args)
    data = LfunctionPlot.paintSvgHolo(args['Nmin'], args['Nmax'], args['kmin'], args['kmax'])
    response = make_response(data)
    response.headers['Content-type'] = 'image/svg+xml'
    return response

def render_browseGraphTMP(args):
    logger.info(args)
    data = LfunctionPlot.paintSvgHoloGeneral(args['Nmin'], args['Nmax'], args['kmin'], args['kmax'],args['imagewidth'], args['imageheight'])
    response = make_response(data)
    response.headers['Content-type'] = 'image/svg+xml'
    return response

def render_browseGraphChar(args):
    data = LfunctionPlot.paintSvgChar(args['min_cond'], args['max_cond'], args['min_order'], arg['max_order'])
    response = make_response(data)
    respone.headers['Content-type'] = 'image/svg+xml'
    return response

def render_lcalcfile(L, url):
    try:  #First check if the Lcalc file is stored in the database
        response = make_response(L.lcalcfile)
    except:
        response = make_response(L.createLcalcfile_ver2(url))

    response.headers['Content-type'] = 'text/plain'
    return response


def render_showcollections_demo():
    connection = pymongo.Connection()
    dbNames = connection.database_names()
    dbList = []
    for dbName in dbNames:
        db = pymongo.database.Database(connection, dbName)
        dbMeta = connection.Metadata
        collectionNames = db.collection_names()
        collList = []
        for collName in collectionNames:
            if not collName == 'system.indexes': 
                collMeta = pymongo.collection.Collection(dbMeta,'collection_data')
                infoMeta = collMeta.find_one({'db': dbName, 'collection': collName})
                try:
                    info = infoMeta['description']
                except:
                    info = ''
                collList.append( (collName, info) )
        dbList.append( (str(db.name), collList) )
    info = {'collections' : dbList}
    return render_template("ShowCollectionDemo.html", info = info)

## NOT USED
##def processDirichletNavigation(args):
##    logger.info(str(args))
##    try:
##        logger.debug(args['start'])
##        N = int(args['start'])
##        if N < 3:
##            N=3
##        elif N > 100:
##            N=100
##    except:
##        N = 3
##    try:
##        length = int(args['length'])
##        if length < 1:
##            length = 1
##        elif length > 20:
##            length = 20
##    except:
##        length = 10
##    try:
##        numcoeff = int(args['numcoeff'])
##    except:
##        numcoeff = 50
##    chars = LfunctionComp.charactertable(N, N+length,'primitive')
##    s = '<table>\n'
##    s += '<tr>\n<th scope="col">Conductor</th>\n'
##    s += '<th scope="col">Primitive characters</th>\n</tr>\n'
##    for i in range(N,N+length):
##        s += '<tr>\n<th scope="row">' + str(i) + '</th>\n'
##        s += '<td>\n'
##        j = i-N
##        for k in range(len(chars[j][1])):
##            s += '<a style=\'display:inline\' href="Character/Dirichlet/'
##            s += str(i)
##            s += '/'
##            s += str(chars[j][1][k])
##            s += '/&numcoeff='
##            s += str(numcoeff)
##            s += '">'
##            s += '\(\chi_{' + str(chars[j][1][k]) + '}\)</a> '
##        s += '</td>\n</tr>\n'
##    s += '</table>\n'
##    return s
##    #info['contents'] = s
##    #return info

def processEllipticCurveNavigation(startCond, endCond):
    try:
        N = startCond
        if N < 11:
            N=11
        elif N > 100:
            N=100
    except:
        N = 11
        
    try:
        if endCond > 500:
            end = 500
        else:
            end = endCond
            
    except:
        end = 100
        
    iso_list = LfunctionComp.isogenyclasstable(N, end)
    s = '<h5>Examples of L-functions attached to isogeny classes of elliptic curves</h5>'
    s += '<table>'
    
    logger.debug(iso_list)

    counter = 0
    nr_of_columns = 10
    for label in iso_list:
        if counter==0:
            s += '<tr>'
            
        counter += 1
        s += '<td><a href="' + url_for('render_Lfunction', arg1='EllipticCurve', arg2='Q', arg3=label)+ '">%s</a></td>\n' % label
            
        if counter == nr_of_columns:
            s += '</tr>\n'
            counter = 0

    if counter>0:
        s += '</tr>\n'
        
    s += '</table>\n'
    return s

def processMaassNavigation():
    s = '<h5>Examples of L-functions attached to Maass forms on Hecke congruence groups $\Gamma_0(N)$</h5>'
    s += '<table>\n'

    s += '<tr>\n'
    s += '<td><bold>N=3:</bold></td>\n'
    s += '<td><a href="' + url_for('render_Lfunction', arg1='ModularForm', arg2='GL2', arg3='Q',
                                   arg4='Maass', arg5='4cb8502658bca9141c00002a', db='FS')+ '">4.38805356322</a></td>\n' 
    s += '<td><a href="' + url_for('render_Lfunction', arg1='ModularForm', arg2='GL2', arg3='Q',
                                   arg4='Maass', arg5='4cb8502658bca9141c00002b', db='FS')+ '">5.09874190873</a></td>\n' 
    s += '<td><a href="' + url_for('render_Lfunction', arg1='ModularForm', arg2='GL2', arg3='Q',
                                   arg4='Maass', arg5='4cb8502658bca9141c00002c', db='FS')+ '">6.12057553309</a></td>\n' 
    s += '<td><a href="' + url_for('render_Lfunction', arg1='ModularForm', arg2='GL2', arg3='Q',
                                   arg4='Maass', arg5='4cb8502658bca9141c00002d', db='FS')+ '">6.75741527775</a></td>\n' 
    s += '<td><a href="' + url_for('render_Lfunction', arg1='ModularForm', arg2='GL2', arg3='Q',
                                   arg4='Maass', arg5='4cb8502658bca9141c00002e', db='FS')+ '">7.75813319502</a></td>\n' 
    s += '</tr>\n'
    
    s += '<tr>\n'
    s += '<td><bold>N=5:</bold></td>\n'
    s += '<td><a href="' + url_for('render_Lfunction', arg1='ModularForm', arg2='GL2', arg3='Q',
                                   arg4='Maass', arg5='4cb8502658bca9141c000036', db='FS')+ '">3.02837629307</a></td>\n' 
    s += '<td><a href="' + url_for('render_Lfunction', arg1='ModularForm', arg2='GL2', arg3='Q',
                                   arg4='Maass', arg5='4cb8502658bca9141c000039', db='FS')+ '">4.89723501573</a></td>\n' 
    s += '<td><a href="' + url_for('render_Lfunction', arg1='ModularForm', arg2='GL2', arg3='Q',
                                   arg4='Maass', arg5='4cb8502658bca9141c00003b', db='FS')+ '">5.70582652719</a></td>\n' 
    s += '<td><a href="' + url_for('render_Lfunction', arg1='ModularForm', arg2='GL2', arg3='Q',
                                   arg4='Maass', arg5='4cb8502658bca9141c00003c', db='FS')+ '">6.05402838077</a></td>\n' 
    s += '<td><a href="' + url_for('render_Lfunction', arg1='ModularForm', arg2='GL2', arg3='Q',
                                   arg4='Maass', arg5='4cb8502658bca9141c00003d', db='FS')+ '">6.45847643848</a></td>\n' 
    s += '</tr>\n'
    
    s += '</table>\n'

    return s
