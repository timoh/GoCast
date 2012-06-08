// Filename: main.js
$(function(){

"use strict";

// -- OVERRUN METHODS --------------------------------------------------------
            

// -- MODELS ------------------------------------------------------------------

    var IdeaAction = Backbone.Model.extend({
        idAttribute : "_id",
        defaults : {
            activator : null,
            action : null,
            subject: null,
            subject_author : null,
            amount : 0.0 ,

        },    
    });

    var User = Backbone.Model.extend({
        idAttribute : "_id",

        defaults : {
            name : "Anonymous",
        },    
    });

    var Item = Backbone.Model.extend({
        idAttribute : "_id",
        initialize : function(){
            this.collection = new ItemCollection; 
        },
        
        url : function(){
            //overrun url for PUT and delete method to support mongoDB id system
            var path =  window.location.href + this.collection.url.slice(1) 
            if(!(_.isUndefined(this.id)) || !this.isNew()){
                //if models already exist in DB, then add ID to url to do update
                path += "/" + this.id["$oid"];
            }

            return path
        },
        defaults : {
                    visibility : 0,
                    punchline: "Item default",
                    content : "changes it later",
                    tags : ["demo", "tag2"],
        },
    });

//-- COLLECTIONS ----------------------------------------------------

    var ItemCollection = Backbone.Collection.extend({
        url :  "/ideas",
        model : Item,
        initialize : function(){
            this.bind("change", this.update, this);

        },

        update : function(){
            console.log("catched changes on collection");
            this.fetch( );           
        },


        comparator: function(item){
            return item.get("position");
        },
    });

    var IdeaActions = Backbone.Collection.extend({
        url : "/actions",
        model : IdeaAction,
    });


    var Users = Backbone.Model.extend({
        url : "/users",
        model : User,
    });

    var LoginUser = Backbone.Model.extend({
        url : "/users/current",
        model : User,
    });


// -- VIEWS  -----------------------------------------------------

    var ItemEditView = Backbone.View.extend({
        el : "#idea-item-edit",
        template : _.template($("#item-edit-template").html()),
        
        events : {
            "click .btn-save" : "saveItem",
            "click .btn-close": "closeView",
        },

        initialize : function(options){
            //collection and model
            this.collection = options.collection;
            this.model = options.models;
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
            $(this.el).modal({keyboard: true, show : true, backdrop : true});

            //finally do bindings between form elements and model
            Backbone.ModelBinding.bind(this);
            return this;
        },

        saveItem : function(){
            console.log("Model vals:")
            console.log(JSON.stringify(this.model));
            this.model.save({},{
                success :  function(model, resp){
                    var feedback_template =  _.template($("#feedback-template").html());
 
                    $(".editor-feedback").html(
                        feedback_template({
                            result : "success", 
                            message : "Idea is saved."}));
                    IdeaApp.Views.IdeaList.render(); 
                },

                error : function(err){
                    console.log(err);

                    $(".editor-feedback").html(
                       model.feedback_template({
                            result : "error",
                            message : "Saving failed!"
                    }));
                }     
            });
           
        },

        closeView : function(){
            $(this.el).modal("hide");
            $(this.el).empty();
            Backbone.ModelBinding.unbind(this);
            IdeaApp.Views.IdeaList.render();
        },
    });

    var ItemView = Backbone.View.extend({
        tagName : "div",
        template : _.template($("#item-template").html()),
        actions :  new IdeaActions,


        events: {
                    "click .upvote" : "upvote",
                    "click .follow" : "follow",
                    "click .share"  : "share",
                    "click .hangout" : "initHangout",
                    "click .invest": "invest",

                    "click .edit-this" : "updateView",
                    "click .translate-this" : "translate",
                    "click .tag-this" : "taggify",
                    "click .flag-this" : "flag",
        },
        
        initialize : function(){
           //this.model.bind("update", this.render, this); 
        },
       
        
        render  : function(){
            console.log("rendering item.");
            console.log(JSON.stringify(this.model));
            $(this.el).empty();
            $(this.el).html(this.template(this.model.toJSON()));
            return this;
        },
        
        update : function(){
            console.log("Updating ...");    
        },

        upvote : function(){
            var callback = function(view){ view.$(".upvote").addClass("active");};
            this.addAction("upvote", callback);
        },
 
        follow : function(){
            console.log("Following");
            var callback = function(view){ view.$(".follow").addClass("active");};
            this.addAction("follow", callback);

        },

        share :  function(){
            console.log("Share it");
            var callback = function(view){ view.$(".share").addClass("active");};
            this.addAction("share", callback);

        },

        initHangout : function(){
            console.log("Initializing hangout");
            var callback = function(view){ view.$(".hangout").addClass("active");};
            this.addAction("hangout", callback);

        },

        invest : function(){
            console.log("Invest into ...");
            var callback = function(view){ view.$(".invest").addClass("active");};
            this.addAction("invest", callback);

        },

       
        addAction: function(action_name, callback){
            var action = new IdeaAction;
            action.set({
                    activator : null, //will be attached by backend
                    action : action_name,
                    subject : this.model.get("_id"),
                    subject_author : this.model.get("author"),
            });
            this.actions.add([action]);
            action.save();
            if(_.isUndefined(callback)){
                var callback = function(){
                    console.log("action"+ action_name  +" added");
                }
            }
            this.actions.fetch({success : callback(this)});

        },

        updateView : function(evt){
            console.log("editing idea...");
            console.log(JSON.stringify(this.model));
            var view = new ItemEditView({model : this.model});
            view.render();
        },

        translate : function(){
            console.log("translate it..");
        },


        taggify : function(){
            console.log("Add tags to idea ...");
        },

        flag : function(){
            console.log("Flag this.");    
        },

        
        saveUpdate : function(){
            console.log('saving ideas');    
        },
        
 
    });


    var ItemListView = Backbone.View.extend({
        el : $("#idea-list"),
        template: _.template($("#item-template").html()),

        initialize : function(options){
            // _.bindAll(this, "render", "add");
        //    this.collection.bind("change", this.render, this);
        },

        render : function(){
            var self = this;
            this.el.empty();
            this.collection.fetch({async : false});
            //render only there is collection defined.
            if(!(_.isUndefined(this.collection))){
                console.log("rendering itemlistview with " + this.collection.length + "elems.")

                this.collection.each(function(idea){
                    var itemview = new ItemView({
                        model : idea, 
                    });                    
                    self.el.append(itemview.render().el);

                });

                IdeaApp.Utils.buildButtons();
            }
            else {
                console.debug("ItemListView.render: Collection is undefined!")
            }
            return this;
        },


    });

    var IdeaMenuView = Backbone.View.extend({
        el :$("#idea-menu"),
        template : _.template($("#idea-menu-template").html()),

        events : {
            "click .new" : "addNewItem",
            "click .sort": "sortItems",
            "click .filter": "filterItems",
        },


        addNewItem : function(){
            console.debug("Adding new idea");
            var new_idea = new Item;
            var ideaEditor = new ItemEditView({
                model : new_idea,
                collection : this.collection,
            });

            ideaEditor.render();
        },

        sortItems : function(){
            console.log("Sorting items");    
        },

        filterItems : function(){
            console.log("Filtering items");    
        },

    });

// -- GLOBAL OBJECT Of CURRENT OBJECT ---------------------------------------------
    var ContentView = Backbone.View.extend({
        
        el : $("idea-content"),

        render : function(){
            var ideas = new ItemCollection;
            var login = new LoginUser; 
            
            var fetch_data = function(settings){
                login.fetch(settings);
                ideas.fetch(settings);
            }
            var render_content = function(){
                var ideaMenu = new IdeaMenuView({collection : ideas});
                var ideaListView = new ItemListView({collection : ideas, login : login});
                IdeaApp.Views.IdeaList = ideaListView;

                ideas.bind('add', function(message){
                    this.fetch({success : function(){ideaListView.render()}})});
                ideas.bind('change', function(message){
                    this.fetch({success : function(){ideaListView.render()}})});
                
                //get ideas and render content
                ideaMenu.render();
                ideaListView.render();
               
            };
            
            //to be sure that initial data is received before rendering.
            fetch_data({async:false});
            $(document).ajaxSuccess(render_content());
            return this;    
        }
    });


    var NavigationRouter = Backbone.Router.extend({
        _data : null,
        _items: null,
        _view: null,

        routes : {
            "ideas1/:id":  "showIdea",
            "#": "main",
        },

        initialize : function(options){
           var view = new ContentView;
            view.render();
            return this;
        },

        main : function(actions){
            var view = new ContentView;
            //this.showIdea(1);    
        },

        showIdea : function(id){
            var view = new ContentView({model : this._items.at(id-1)});
            $(".active").removeClass("active");
            $("#item"+ id).addClass("active");
            view.render();
        },
    });

// -- APP INIT AND UTILS ------------------------------------------------------
    var IdeaApp = {
        Models : {},
        Views : {},
        Utils : {},
    };


    //button builder for menu buttons
    IdeaApp.Utils.buildButtons = function(){
            $(".btn").each(function(id,btn){
                var icon = $(this).attr('icon');
                // $(this).removeClass(icon);
                if(icon){
                    $(this).button({icons: {primary : icon}, });
                }
            });
    }

// -- MAIN --------------------------------------------------------------------
    var App = new NavigationRouter;
    Backbone.history.start();

});
