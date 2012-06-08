$(function(){
	"use strict;"

	var Top = {
		Collections : {},
		Views : {},
		Routers : {}
	}

	var TopModel = Backbone.View.extend({
		idAttribute : "_id",
	});

	var TopCollection = Backbone.Collection.extend({
		//model : TopModel,
		tagName : "div",
		
		initialize : function(options){
			if(!(_.isUndefined(options.url))){
				this.url = options.url
			}
		},
	});

	var TopView = Backbone.View.extend({
		el : "div",
		template :  _.template($("#toplist-template").html()),

		initialize : function(options){
			if(!(_.isUndefined(options.category))){
				this.category = options.category;
			}
		},

		render : function(){
			if(_.isUndefined(this.collection)){
				console.debug("Collection is udefined, there is nothing to render");
				return ;
			}

			console.debug("rendering content");

			$("#toplist-container").append(
				this.template({
					category : this.category || "Category", 
					toplist: this.collection.toJSON()})
			);

			return this;
		},
	});

	var TopRouter = Backbone.Router.extend({
		routes : {
			"/" : "showToplists",
		},

		showToplists : function(){
			console.debug("Rendering lists");
			if(!(_.isUndefined(Top.Views.Ideas))){
				Top.Collections.Ideas.fetch({
					success : function(){
						Top.Views.Ideas.render();
					}
				});
				
			}
			else{
				console.debug("View 'Ideas' is undefined.");
			}
			
		},

	});

	Top.Collections.Ideas = new TopCollection({url : "/top/ideas"});
	Top.Collections.Investors = new TopCollection({url : "/top/investors"});
	Top.Collections.Latest = new TopCollection({url : "/top/latest"});

	Top.Views.Ideas  = new TopView({
		category : "Top Ideas",
		model : new TopModel, 
		collection : Top.Collections.Ideas});
	Top.Views.Investors  = new TopView({
		category : "Top Investors",
		model : new TopModel, 
		collection : Top.Collections.Investors});
	Top.Views.Latest  = new TopView({
		category : "Latest Ideas",
		model : new TopModel, 
		collection : Top.Collections.Latest});

	Top.Routers.Main = new TopRouter;
	Top.Collections.Ideas.fetch({success : function(){Top.Views.Ideas.render()}});
	Top.Collections.Investors.fetch({success : function(){Top.Views.Investors.render()}});
	Top.Collections.Latest.fetch({success : function(){Top.Views.Latest.render()}});
	
});