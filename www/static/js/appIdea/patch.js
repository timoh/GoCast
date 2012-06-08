
var PatchApp = {
	Models : {},
	Collections : {},
	Views : {},
	Routers : {},
	app : null,
};

$(function(){
	
	"use strict";

	//-- Models ---------------------------------------------------------------
	PatchApp.Models.Revision = Backbone.Model.extend({

	});

	PatchApp.Models.Chat = Backbone.Model.extend({
	})

	PatchApp.Models.Voting =  Backbone.Model.extend({
		urlRoot : "",
		url : function(){
			return this.urlRoot + "/voting";
		},

		initialize :  function(options){
			if(!(_.isUndefined(options.urlRoot))){
				this.urlRoot = options.urlRoot;
			}
		},
	});

	PatchApp.Collections.Revisions = Backbone.Collection.extend({
		model : PatchApp.Models.Revision,
		urlRoot : "",

		initialize : function(options){

			if(options && !(_.isUndefined(options.urlRoot))){
				this.urlRoot = options.urlRoot;
			} else {
				this.urlRoot = window.location.href;
			}

			if(options && !(_.isUndefined(options.pageSize))){
				this.pageSize = options.pageSize;
			}
			else{
				this.pageSize = 10;
			}

			if(options && !(_.isUndefined(options.pageStartIndex))){
				this.pageStartIndex = options.pageStartIndex;
			}
			else{
				this.pageStartIndex = 10;
			}

		},

		url :  function(){
			return this.urlRoot + "/revisions"
		}, 
	});

	PatchApp.Collections.Chat = Backbone.Collection.extend({
		url : function(){
			var url = this.urlRoot + '/chats';
			return url; //idea/:id/revisions/:rid/chats
		},

		initialize : function(options){
			if(!(_.isUndefined(options.urlRoot))){
				this.urlRoot = options.urlRoot;
			}
		},
	});


	//-- VIEWS ----------------------------------------------------------------
	//?is it necessary
	
	PatchApp.Views.Chat = Backbone.View.extend({
		el : $("#chat-container"),
		template : _.template($("#chat-template").html()),

		render : function(){
			this.el.html(
				this.template(this.collection.toJSON()));
		},
	});

	PatchApp.Views.Voting = Backbone.View.extend({
		el : $("#voting-container"),
		template : _.template($("#voting-template").html()),

		render :  function(){
			this.el.html(
				this.template(this.model.toJSON()));
		},
	});


	
	PatchApp.Views.Revision = Backbone.View.extend({
		el : "#revision",
		template : _.template($("#revision-template").html()),

		initialize : function(options){
			
		},
		render : function(){
			console.log("Revisions urlRoot: " + this.collection.urlRoot);
			this.collection.fetch({async : false})
			$(this.el).html(
				this.template(this.collection.at(0).toJSON()));
			//this.chatView.render();
			//this.votingView.render();
		},
	});

	// -- ROUTER ------------------------------------------------------------
	PatchApp.Routers.Main = Backbone.Router.extend({
		initialize : function(){
			
		},

		routes : {
			"" : "renderContent",
		},

		renderContent : function(){
			console.log("rendering main content");
			var lof = window.location.pathname.lastIndexOf("/");
			var idea_id = window.location.pathname.slice(lof + 1);
			var revisions = new PatchApp.Collections.Revisions({urlRoot : "/ideas/"+ idea_id })
			var revView = new PatchApp.Views.Revision({collection :  revisions});
			revView.render();

		}
	});

	PatchApp.main = new PatchApp.Routers.Main;
	Backbone.history.start();


});