$(function(){

	var HomeApp  = {
		Views : {},
		Models : {},
		Collections: {},
		Routers : {}
	}

//-- Model --------------------------------------------------------------------

	var User = Backbone.Model.extend({
		idAttribute : "_id",
		url : "/users/current"

	});

	var Idea = Backbone.Model.extend({
		idAttribute : "_id.$oid",
		defaults : {
                    visibility : 0,
                    punchline: "Item default",
                    content : "changes it later",
                    tags : [],
        },
	});

	var Tag = Backbone.Model.extend({});

//-- Collections --------------------------------------------------------------
	var Ideas = Backbone.Collection.extend({
		url : "/ideas/user/1",
		model : Idea,

	});

	var Tags = Backbone.Collection.extend({
		model : Tag, 
	})
//-- Views --------------------------------------------------------------------
	var Profile = Backbone.View.extend({
		el : "#profile",
		template : _.template($("#profile-template").html()),

		render : function(){
			this.model.fetch({async : false});
			console.debug(JSON.stringify(this.model));
			$(this.el).html(this.template({user: this.model.toJSON()}));
		}
	})

	var IdeaList = Backbone.View.extend({
		el : "#idea-list",
		template : _.template($("#idea-list-template").html()),
		

		render : function(){
			this.collection.fetch({async : false});
			$(this.el).html(
				this.template({"ideas" : this.collection.toJSON()})
			);
			this.activatePopOvers();
			$('.tabs').tabs(); //activate tabs
		},

		addNew : function(){
			console.log("Creating new idea.");
			var editor = new ItemEditView({
				model : new Idea,
				collection : this.collection})
			//editor.render();
		},

		activatePopOvers : function () {
          $("a[rel=popover]")
            .popover({ offset: 10, html : true, placement : "below", })
            .click(function(e) {e.preventDefault()});
        }, 

	});

	var TagCloud = Backbone.View.extend({
		el : "#tags",
		template : _.template($("#tags-template").html()),
	
		render : function(){
			$(this.el).html(this.collection.toJSON().join(", "))
		},
	});

	var ItemEditView = Backbone.View.extend({
	        el : "#idea-editor-modal",
	        template : _.template($("#idea-editor-template").html()),
	        
	        events : {
	            "click .btn-save" : "saveItem",
	            "click .btn-close": "closeView",
	        },

	        initialize : function(options){
	            //collection and model
	            this.collection = options.collection;
	            this.model = options.model;
	            this.render();
	        },

	        render : function(){
	            $(this.el).empty();
	            console.debug("Got this model for editing");
	            console.debug(JSON.stringify(this.model));
	            if(_.isUndefined(this.model)){
	                //if user didnt gave model,then define it as new model - use default values;
	                console.log("Model was undefined");
	                this.model = new Item;
	                return this;
	            }
	            
	            if(this.model.isNew()){
	                console.log("Using unsaved model.")    
	            }
	            $(this.el).html(this.template(this.model.toJSON()));
	            $('#idea-tags').tagsInput(); //active tag input
	            
	            $(this.el).modal({keyboard: true, show : true, backdrop : true});

	            //finally do bindings between form elements and model
	            Backbone.ModelBinding.bind(this);
	            return this;
	        },

	        saveItem : function(){
	            console.log("Model vals:")
	            console.log(JSON.stringify(this.model));
	            this.collection.create(this.model.toJSON());
	            
	           
	        },

	        closeView : function(){
	            $(this.el).modal("hide");
	            $(this.el).empty();
	            Backbone.ModelBinding.unbind(this);
	            HomeApp.Views.IdeaList.render();
	        },
	    });



//-- App initializing
	var Router = Backbone.Router.extend({
		initialize : function(){
			HomeApp.Views.Profile = new Profile({model : new User});
			HomeApp.Views.IdeaList = new IdeaList({collection : new Ideas});
			HomeApp.Views.TagCloud = new TagCloud({});
			HomeApp.Views.Profile.render();
			HomeApp.Views.IdeaList.render();
		},

		routes : {
			"" : "index",
			"addNew" : "addNewIdea",
			"addNew" : "addNewIdea",
			"#addNewIdea" : "addNewIdea"
		},

		index : function(){
			console.log("Rendering router's index")
			
		},

		addNewIdea : function(){
			console.log("Going to add new idea:");
			HomeApp.Views.IdeaList.addNew();	
		}
	});

	
	HomeApp.Routers.main = new Router;
	Backbone.history.start();

});