/* eslint-env node */

const path = require('path');
const webpack = require('webpack');

const dotenv = require('dotenv').config({path: path.join(__dirname, 'react.env')});

module.exports = {
    entry: './scripts/Main.jsx',
    output: {
        path: __dirname,
        filename: './static/script.js'
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                loader: 'style-loader!css-loader'
            },
            {
                test: /\.s[ac]ss$/i,
                use: [
                  // Creates `style` nodes from JS strings
                  'style-loader',
                  // Translates CSS into CommonJS
                  'css-loader',
                  // Compiles Sass to CSS
                  'sass-loader',
                ],
            },
            {
                test: /\.(js|jsx)$/,
                exclude: /(node_modules)/,
                loader: 'babel-loader',
                options: {
                    presets: [
                        '@babel/preset-react',
                        [
                            '@babel/preset-env',
                            {
                                targets: {
                                    esmodules: false
                                }
                            }
                        ]
                    ]
                }
            }
        ]
    },
    resolve: {
        extensions: ['.js', '.jsx'],
    },
    plugins: [
        new webpack.EnvironmentPlugin(Object.keys(dotenv.parsed || {}))
    ]
};
