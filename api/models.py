# import db from api module
from api import db


# Define a base model for other database tables to inherit
class HyperParams(db.Model):
    __tablename__ = 'hyper_parameters'

    id = db.Column(db.Integer, primary_key=True)
    lr = db.Column(db.Float, nullable=False)
    epoch = db.Column(db.Integer, nullable=False)
    hidden_nodes = db.Column(db.Integer, nullable=False)
    model_name = db.Column(db.String(80), nullable=False)
    accuracy = db.Column(db.Float, nullable=False)
    graph_plot_id = db.Column(db.Integer, db.ForeignKey('graph_plot.id'),
                              nullable=False)
    graph_plot = db.relationship('ModelGraphdata', backref='hyper_parameters',
                                 uselist=False)

    def __repr__(self):
        return '<Model %r>' % self.model_name


class ModelGraphData(db.Model):
    __tablename__ = 'grah_plot'

    id = db.Column(db.Integer, primary_key=True)
    lr_vs_p = db.Column(db.String(80), nullable=False)
    epoch_vs_p = db.Column(db.String(80), nullable=False)
    hn_vs_p = db.Column(db.String(80), nullable=False)

    def __repr__(self):
        return'<Model %r>' % self.id
