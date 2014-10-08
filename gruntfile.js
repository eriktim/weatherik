module.exports = function(grunt) {

  grunt.initConfig({
    pkg: grunt.file.readJSON('package.json'),
    jshint: {
      files: [
        'gruntfile.js',
        'tasks/**/*.js',
      ]
    }
  });

  grunt.loadNpmTasks('grunt-contrib-jshint');

  grunt.registerTask('lint', ['jshint']);

  grunt.registerTask('default', ['lint']);

};
