# resources/tag.py

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError

from restapi.models import TagModel, StoreModel, ItemModel
from restapi.schemas.schemas import TagSchema, TagAndItemSchema
from restapi.db import db

blp = Blueprint("Tags", "tags", __name__, description="Operations on tags")

@blp.route("/store/<int:store_id>/tag")
class TagsInStore(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, store_id):
       store = StoreModel.query.get_or_404(store_id)
       return store.tags.all()
    
    @blp.arguments(TagSchema)
    @blp.response(201, TagSchema(many=True))
    def post(self, tag_data, store_id):
        if TagModel.query.filter(TagModel.store_id == store_id, TagModel.name == tag_data["name"]).first():
            abort(400, message="A tag that name alrady exists in that store.")
        tag = TagModel(**tag_data, store_id=store_id)
        try:
            db.session.add(tag)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(500, message=str(e))

        return tag    

@blp.route("/item/<int:item_id>/tag/<int:tag_id>")
class LinkTagsToItem(MethodView):
    @blp.response(201, TagSchema)
    def post(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.append(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(404, message = str(e))
        
        return tag
    
    @blp.response(201, TagSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)

        item.tags.remove(tag)

        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError as e:
            abort(404, message = str(e))
        
        return {"message" : "item removed from the tag", "item" : item, "tag" : tag}
    

@blp.route("/tag/<int:tag_id>")
class Tag(MethodView):
    @blp.response(200, TagSchema)
    def get(self, tag_id):
       tag = TagModel.query.get_or_404(tag_id)
       return tag

    @blp.response(200, 
                  description="Deletes a tag if no item is tagged",
                  example={"message" : "Tag deleted"}
                  )
    @blp.alt_response(404,
                      description="Tag not found")
    @blp.alt_response(400,
                      description="returned if teh tag is assigned to one or more items. in this case the tag is not deleted")
    def delete(self, tag_id):
       tag = TagModel.query.get_or_404(tag_id)
       
       if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message" : "tag deleted"}
       abort(400,
             message="could not delete the tag. Make sure tag is not associated with any items, then try again.")
