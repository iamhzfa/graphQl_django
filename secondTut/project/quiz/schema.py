import graphene
from graphene_django import DjangoObjectType, DjangoListField
from .models import Category, Quizzes, Question, Answer

class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")

class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id", "title", "category", "quiz")

class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("id", "title", "quiz")

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text")

class Query(graphene.ObjectType):
    # all_quiz = DjangoListField(QuizzesType)
    # def resolve_quiz(root, info):
    #     return f"This is first question"
    # all_quizzes = graphene.List(QuizzesType)
    all_quizzes = graphene.Field(QuizzesType, id=graphene.Int())
    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())
    def resolve_all_quizzes(self, info, id):
        return Quizzes.objects.get(pk=id)
    def resolve_all_questions(self, info, id):
        return Question.objects.get(pk=id)
    def resolve_all_answers(self, info, id):
        return Answer.objects.filter(question__id=id)


class CreateCategoryMutation(graphene.Mutation):

    class Arguments:
        name = graphene.String(required=True)
    category = graphene.Field(CategoryType)
    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CreateCategoryMutation(category=category)

class UpdateCategoryMutation(graphene.Mutation):

    class Arguments:
        id = graphene.Int()
        name = graphene.String(required=True)
    category = graphene.Field(CategoryType)
    @classmethod
    def mutate(cls, root, info, id, name):
        category = Category.objects.get(id=id)
        category.name = name
        category.save()
        return UpdateCategoryMutation(category=category)

class DeleteCategoryMutation(graphene.Mutation):

    class Arguments:
        id = graphene.Int()
    category = graphene.Field(CategoryType)
    @classmethod
    def mutate(cls, root, info, id):
        category = Category.objects.get(id=id)
        category.delete()
        return

class Mutation(graphene.ObjectType):
    add_category = CreateCategoryMutation.Field()
    update_category = UpdateCategoryMutation.Field()
    delete_category = DeleteCategoryMutation.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
