module.exports = function(grunt) {
    'use strict';

    var jsFileList = [];

    grunt.loadNpmTasks('grunt-contrib-jshint');
    grunt.loadNpmTasks('grunt-contrib-concat');

    grunt.initConfig({

        pkg: grunt.file.readJSON('package.json'),

        jshint: {
            options: {
                jshintrc: '.jshintrc'
            },
            all: [
                'Gruntfile.js',
                'nomadboard/nomadboard/static/js/*.js'
            ]
        },

        sass: {
            dev: {
                files: {
                    'nomadboard/nomadboard/static/css/main.css': 'nomadboard/nomadboard/static/scss/main.scss',
                },
                options: {
                    sourcemap: true
                },
            }
        },

        concat: {
            options: {
                separator: ';\n'
            },
            dist: {
                src: ['nomadboard/nomadboard/static/js/{,*/}*.js'],
                dest: 'nomadboard/nomadboard/static/js/scripts.js',
            },
        },

        watch: {
            sass: {
                files: ['nomadboard/nomadboard/static/scss/{,*/}*.{scss,sass}'],
                tasks: ['sass:dev']
            },
            js: {
                files: [
                    jsFileList,
                    '<%= jshint.all %>'
                ],
                // tasks: ['jshint', 'concat']
            },
            livereload: {
                options: {
                    livereload: false
                },
                files: [
                    'nomadboard/nomadboard/static/css/main.css',
                    'nomadboard/nomadboard/static/js/main.js',
                ]
            }
        }

    });

    grunt.loadNpmTasks('grunt-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');

    grunt.registerTask('default', ['jshint', 'sass:dev']);
};
