#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_gif_component as gif

from dash.dependencies import Input, Output,State

from ants import *

#alg(num_iterations, num_ants, evap_rate,Q_const, alpha, beta,size_graph)

# import the css template, and pass the css template into dash
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.title = "Ant Optimization Demo"


server = app.server

g_num_ants = 4
g_evap_rate = .2
g_Q_const  = 1
g_alpha = 1
g_beta = 1
g_num_iterations = 100
g_num_nodes = 10

class Constants:
    def __init__():
        self.num_ants = 4
        self.evap_rate = .2
        self.Q_const  = 1
        self.alpha = 1
        self.beta = 1
        self.num_iterations = 100
        self.num_nodes = 10


app.layout = html.Div([
    #########################Title
    html.Div([html.H1("Ant Optimization Demonstration"), 

              html.H5("Sofia Hurtado, Unconventional Computing SP2021")
             
        ],
             className="row",
             style={'textAlign': "center"}),
    
    #############################################################################################define the row
    
    #paragraph about ant optimization 



    #applications 


    #demo 
    ################################################################################################

    html.Div([

        html.Div(id='exp_gif'),

        html.Div(id='gif_viewer', children=[

            gif.GifPlayer(
                gif='assets/aco.gif',
                still='assets/still.png',
            ), 

            ], style={'display':'inline-block'}),
        
    
        ######################### input div: num_nodes ############################
        html.Div( children=[
            
            #html.Div(id='container-button-basic',
            html.Button('Run Simulation', id='run_simulation', n_clicks=0),


            html.Div(id='sim_status',style={'display':'inline-block', 'margin-right':"10px"}, 

                    children=[ "Status: Completed sim_run: 0"]),


            html.Div( style = {'display':'block' },
            children = [

                html.Div(id='num_node_basic',style={'display':'block', 'margin-right':"10px"}, 

                    children=[ "Number of Nodes: {}".format(str(g_num_nodes))]),
            
                    html.Div([
                        html.Details([
                            html.Summary('Update'),
                            html.Div(dcc.Input(id='input-nodes-on-submit', type='number')),
                            html.Button('Submit', id='submit-node-val', n_clicks=0)
                        ])
                    

                         ], style={'display':'inline-block'}),

                    dcc.Store(id='number_of_nodes_data', children=[]),


                ########################## input div: num_ants ############################
                
                html.Div(id='num_ants',style={'display':'block', 'margin-right':"10px"}, 

                    children=[ "Number of ants: {}".format(str(g_num_ants))]),
                    
                    html.Div([
                        html.Details([
                            html.Summary('Update'),
                            html.Div(dcc.Input(id='input-ants-on-submit', type='number')),
                            html.Button('Submit', id='submit-ants-val', n_clicks=0)
                        ]) ], style={'display':'inline-block'}),

                    dcc.Store(id='num_ants_data', children = []),


                
                ########################## input div: num_iterations ############################
                html.Div(id='num_iterations',style={'display':'block', 'margin-right':"10px"}, 

                    children=[ "Number of iterations: {}".format(str(g_num_iterations))]),
                    
                    html.Div([
                        html.Details([
                            html.Summary('Update'),
                            html.Div(dcc.Input(id='input-iters-on-submit', type='number')),
                            html.Button('Submit', id='submit-iters-val', n_clicks=0)
                        ]) ], style={'display':'inline-block'}),
                    
                    dcc.Store(id='iters_data', children = []),


                ########################## input div: evap_rate ############################
                html.Div(id='evap_rate',style={'display':'block', 'margin-right':"10px"}, 

                    children=[ "Pheromone Evaporation Rate: {}".format(str(g_evap_rate))]),
                    
                    html.Div([
                        html.Details([
                            html.Summary('Update'),
                            html.Div(dcc.Input(id='input-evap-on-submit', type='number')),
                            html.Button('Submit', id='submit-evap-val', n_clicks=0)
                        ]) ], style={'display':'inline-block'}),

                    dcc.Store(id='evap_rate_data', children = []),

                ########################## input div: alpha ############################
                html.Div(id='alpha',style={'display':'block', 'margin-right':"10px"}, 

                    children=[ "alpha: {}".format(str(g_alpha))]),
                    
                    html.Div([
                        html.Details([
                            html.Summary('Update'),
                            html.Div(dcc.Input(id='input-alpha-on-submit', type='number')),
                            html.Button('Submit', id='submit-alpha-val', n_clicks=0)
                        ]) ], style={'display':'inline-block'}),
            
                    dcc.Store(id='alpha_data', children = []),

                ########################## input div: beta ############################
                html.Div(id='beta',style={'display':'block', 'margin-right':"10px"}, 

                    children=[ "beta: {}".format(str(g_beta))]),
                    
                    html.Div([
                        html.Details([
                            html.Summary('Update'),
                            html.Div(dcc.Input(id='input-beta-on-submit', type='number')),
                            html.Button('Submit', id='submit-beta-val', n_clicks=0)
                        ]) ], style={'display':'inline-block'}),

                    dcc.Store(id='beta_data', children=[]),


                ########################## input div: Q_const ############################
                html.Div(id='Q',style={'display':'block', 'margin-right':"10px"}, 

                    children=[ "Q: {}".format(str(g_Q_const))]),
                    
                    html.Div([
                        html.Details([
                            html.Summary('Update'),
                            html.Div(dcc.Input(id='input-Q-on-submit', type='number')),
                            html.Button('Submit', id='submit-Q-val', n_clicks=0)
                        ]) ], style={'display':'inline-block'})

                    
   
            ]),

                    dcc.Store(id='Q_data', children=[])

            ], style={'display':'inline-block'}, 


        )
    
    ], style={'display':'inline-block'})
])



###################################callback for left side components

@app.callback(
    
    [dash.dependencies.Output('num_node_basic', 'children'),
    dash.dependencies.Output('number_of_nodes_data', 'data')],

    [dash.dependencies.Input('submit-node-val', 'n_clicks')],
    [dash.dependencies.State('input-nodes-on-submit', 'value')])

def update_nodes(n_clicks, value):
    #v = value + 1
    #global g_num_nodes
    #g_num_nodes = value
    #params.update_nodes(value)
    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update

    return 'Number of Nodes: {}'.format(value), value

@app.callback(
    #dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Output('num_ants', 'children'),
    dash.dependencies.Output('num_ants_data', 'data')],

    [dash.dependencies.Input('submit-ants-val', 'n_clicks')],
    [dash.dependencies.State('input-ants-on-submit', 'value')])

def update_ants(n_clicks, value):

    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update
    
    return 'Number of ants: {}'.format(value),value

@app.callback(
    [dash.dependencies.Output('num_iterations', 'children'),
     dash.dependencies.Output('iters_data', 'data')],
    [dash.dependencies.Input('submit-iters-val', 'n_clicks')],
    [dash.dependencies.State('input-iters-on-submit', 'value')])

def update_iters(n_clicks, value):

    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update
    
    return 'Number of iterations: {}'.format(value),value

@app.callback(
    #dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Output('evap_rate', 'children'),
    dash.dependencies.Output('evap_rate_data', 'data')],
    [dash.dependencies.Input('submit-evap-val', 'n_clicks')],
    [dash.dependencies.State('input-evap-on-submit', 'value')])

def update_evap(n_clicks, value):

    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update
    
    return 'Evaporation rate: {}'.format(value),value


@app.callback(
    #dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Output('alpha', 'children'),
    dash.dependencies.Output('alpha_data', 'data')],
    [dash.dependencies.Input('submit-alpha-val', 'n_clicks')],
    [dash.dependencies.State('input-alpha-on-submit', 'value')])


def update_alpha(n_clicks, value):
    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update
    
    return 'alpha: {}'.format(value),value


@app.callback(
    #dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Output('beta', 'children'),
    dash.dependencies.Output('beta_data', 'data')],
    [dash.dependencies.Input('submit-beta-val', 'n_clicks')],
    [dash.dependencies.State('input-beta-on-submit', 'value')])


def update_beta(n_clicks, value):

    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update
    
    return 'beta: {}'.format(value),value

@app.callback(
    #dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Output('Q', 'children'),
    dash.dependencies.Output('Q_data', 'data')],
    [dash.dependencies.Input('submit-Q-val', 'n_clicks')],
    [dash.dependencies.State('input-Q-on-submit', 'value')])


def update_Q(n_clicks, value):
    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update
    
    return 'Q: {}'.format(value),value


@app.callback(
    Output('exp_gif', 'children'),
    [Input('run_simulation', 'n_clicks')],
    
    [ State('number_of_nodes_data', 'data'),
     State('iters_data', 'data'),
     State('num_ants_data', 'data'),
     State('evap_rate_data', 'data'),
     State('alpha_data', 'data'),
     State('beta_data', 'data'),
     State('Q_data', 'data')
    ]
   )

def run_sim(n_clicks, num_nodes,num_iterations,num_ants, evap_rate,alpha,beta,Q): #, iterations, num_nodes,num_ants,evap,alpha,beta,Q):
    
    if dash.callback_context.triggered[0]["prop_id"] == ".":
        return dash.no_update
    
    #consts = Constants()
    print("num_nodes: ", num_nodes)

    if num_nodes == None:
        num_nodes = 10
    if num_iterations == None:
        num_iterations = 50
    if num_ants == None:
        num_ants = 4
    if evap_rate == None:
        evap_rate = .2
    if alpha == None:
        alpha = 1
    if beta == None:
        beta = 1
    if Q == None:
        Q = 1

    print("ABOUT TO RUN SIMULATION, n_clicks = ", n_clicks)
        
    print("number of nodes: ", num_nodes)
    print("num_iterations: ", num_iterations)
    print("num_ants: ", num_ants)
    print("evap_rate: ", evap_rate)
    print("alpha: ", alpha)
    print("beta: ", beta)
    print("Q: ", Q)

    alg(num_iterations, num_ants, evap_rate, Q, alpha, beta,num_nodes, n_clicks)
    
    print("RAN SIMULATION")

    #will this refresh the gif thing?
    fname_gif = "assets/aco_" + str(n_clicks) + ".gif"
    fname_still = "assets/still_"  + str(n_clicks) + ".png"

    print("loading : ", fname_gif)
    print("and: ", fname_still)

    return gif.GifPlayer( gif=fname_gif, still=fname_still)
    #'Status: Completed sim_run: {}'.format(n_clicks)


if __name__ == '__main__':
    app.run_server(debug=True)