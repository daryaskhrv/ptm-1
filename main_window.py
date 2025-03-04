import os 
import sys

from PyQt6 import QtGui
from PyQt6.QtCore import QSize
from PyQt6.QtWidgets import (QPushButton, QInputDialog, QApplication, 
                             QMainWindow, QFileDialog, QLabel)

from annotation import Annotation 
from annotation_iterator import AnnotationIterator as AnnIt
from copy_dataset import copy_and_annotation, random_copy 
from creat_ann import creat_annotation


class MainWindow(QMainWindow):

    def __init__(self) -> None:
        """Constructor"""
        super(MainWindow, self).__init__()
        self.initUI()

    def initUI(self) -> None:
        """Sets window parameters"""
        self.setWindowTitle("Work with dataset")
        self.setStyleSheet("background-color : #FFDEAD")
        self.setMinimumSize(800, 400)
        self.folder_path = QFileDialog.getExistingDirectory(
            self, 'Выберите папку исходного датасета')
        annotation = Annotation("tmp.cvs")
        creat_annotation(self.folder_path, annotation)
        iter_ann = AnnIt(annotation)
        src = QLabel(f'Исходный датасет:\n{self.folder_path}', self)
        src.setStyleSheet("color : #800000")
        src.setFixedSize(QSize(250, 50))
        src.move(5, 0)
        
        button_create_annotation = self.add_button("Сформировать аннотацию", 
                                                   250, 50, 5, 50)
        button_create_annotation.clicked.connect(self.create_annotation)
        button_create_annotation.setStyleSheet("background-color : #FFA07A")

        button_copy_dataset = self.add_button("Скопировать датасет", 
                                              250, 50, 5, 100)
        button_copy_dataset.clicked.connect(self.dataset_copy)
        button_copy_dataset.setStyleSheet("background-color : #FFA07A")

        button_copy_random_dataset = self.add_button("Рандом датасета", 
                                                     250, 50, 5, 150)
        button_copy_random_dataset.clicked.connect(self.dataset_random)
        button_copy_random_dataset.setStyleSheet("background-color : #FFA07A")

        next_zebra_button = self.add_button("Следующая зебра", 250, 50, 5, 200)
        next_zebra_button.clicked.connect(
             lambda label="zebra", 
             iter=iter_ann:self.next_image("zebra", iter_ann))
        next_zebra_button.setStyleSheet("background-color : #D8BFD8")

        next_horse_button = self.add_button("Следующая лошадь", 250, 50, 5, 250)
        next_horse_button.clicked.connect(
             lambda label="bay horse", 
             iter=iter_ann:self.next_image("bay horse", iter_ann))
        next_horse_button.setStyleSheet("background-color : #D8BFD8")
        
        self.image = QLabel(
             'Нажмите кнопку "Следующая лошадь" или "Следующая зебра".', self)
        self.image.setStyleSheet("color : #800000")
        self.image.resize(400, 300)
        self.image.move(280, 60)
        self.show()

    def add_button(self, name: str, size_x: int, 
                   size_y: int, pos_x: int, pos_y: int) -> QPushButton:
        """Add button with a fixed size and position"""
        button = QPushButton(name, self)
        button.setFixedSize(QSize(size_x, size_y))
        button.move(pos_x, pos_y)
        return button

    def create_annotation_main(self) -> None:
        """Creat annotation of the dataset with chosen name"""
        text, ok = QInputDialog.getText(self, 'Ввод',
            'Введите название файла-аннотации:')
        if ok:
            annotation = Annotation( f"{str(text)}.cvs")
            creat_annotation(self.folder_path, annotation)

    def dataset_copy(self) -> None:
        """Copying dataset (dataset/class_0000.jpg) 
        and creating an annotation
        """
        path_copy = QFileDialog.getExistingDirectory(
            self, 'Введите путь к папке, в которую будет скопирован датасет')
        if not path_copy:
            return
        text, ok = QInputDialog.getText(
            self, 'Ввод', 'Введите название файла-аннотации:')
        if ok:
            annotation = Annotation( f"{str(text)}.cvs")
            copy_and_annotation(self.folder_path, path_copy, annotation)

    def dataset_random(self) -> None:
        """Copying dataset (dataset/номер.jpg) and creating an annotation"""
        path_copy = QFileDialog.getExistingDirectory(
            self, 'Введите путь к папке, в которую будет скопирован датасет')
        if not path_copy:
            return
        text, ok = QInputDialog.getText(self, 'Ввод',
            'Введите название файла-аннотации:')
        if ok:
            annotation = Annotation( f"{str(text)}.cvs")
            random_copy(self.folder_path, path_copy, annotation)

    def next_image(self, label: str, iter: AnnIt) -> None:
        """Shows following picture"""
        try:
            imagePath = iter.__next__(label)
            pixmap = QtGui.QPixmap(imagePath)
            self.image.setPixmap(pixmap)
            self.resize(pixmap.size())
            self.adjustSize()
        except StopIteration:
            self.image.setText(f"Изображения {label} закончились.")
        except OSError:
            print("error")

    def closeEvent(self, event) -> None:
        """Overriding method to delete temporary file"""
        os.remove("tmp.cvs")
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    app.exec()